/* Read-only compatibility model for the vendor Fluidd Control Box. */
const QidiBoxWebStatus = (() => {
  const owns = (object, key) => object != null && Object.prototype.hasOwnProperty.call(object, key);
  const flag = value => value === true || value === 1 || value === "1" ? true
    : value === false || value === 0 || value === "0" ? false : undefined;
  const text = value => typeof value === "string" ? value : "";
  const count = value => Number.isInteger(value) && value >= 0 && value <= 4 ? value : undefined;
  const slotNumber = value => typeof value === "string" && /^slot(?:[0-9]|1[0-6])$/.test(value)
    ? Number(value.slice(4)) : undefined;

  function color(value) {
    if (Array.isArray(value)) value = value[0];
    if (typeof value !== "string") return "";
    const hex = value.replace(/^#/, "");
    return /^[0-9a-f]{6}$/i.test(hex) ? "#" + hex.toUpperCase() : "";
  }

  function flatMaterial(box, index) {
    const prefix = `box${Math.floor(index / 4)}_filament_info_${index % 4}_`;
    if (!owns(box, prefix + "filament_id") && !owns(box, prefix + "filament_type")) return null;
    return Object.fromEntries(["filament_id", "filament_type", "filament_str", "vendor_str", "color_rgb_str", "box_max_temp"]
      .map(key => [key, box[prefix + key]]));
  }

  function variables(status, legacy) {
    const extras = status.box_extras || {};
    const controller = status.multi_color_controller || {};
    const box = controller.box || controller;
    const boxes = Array.isArray(extras.boxes) ? extras.boxes : [];
    let boxCount = count(box.box_count) ?? count(legacy.boxCount) ?? 0;
    if (!owns(box, "box_count") && boxes.length) {
      const lastOnline = boxes.reduce((last, item, index) => flag(item?.is_online) === true ? index : last, -1);
      if (lastOnline >= 0) boxCount = Math.min(4, lastOnline + 1);
    }
    const slots = Array.isArray(legacy.slot) ? legacy.slot.slice(0, 17) : new Array(17).fill(0);
    const records = new Array(17).fill(null);
    let modernMaterials = false;
    for (let index = 0; index < boxCount * 4; index++) {
      const unit = Math.floor(index / 4), tray = index % 4, nested = boxes[unit];
      const material = nested?.filament_info?.[tray] ?? flatMaterial(box, index);
      if (material && typeof material === "object") {
        records[index] = material;
        modernMaterials = true;
      }
      const present = flag(nested?.[`box_inserted_${tray}`]) ?? flag(box[`box${unit}_box_inserted_${tray}`]);
      const online = flag(nested?.is_online) ?? flag(box[`box${unit}_is_online`]);
      if (online === false) slots[index] = 0;
      else if (present !== undefined) slots[index] = present ? 1 : 0;
    }
    const external = controller.extra?.filament_info;
    if (external && typeof external === "object") records[16] = external;
    let loaded = legacy.slotSync;
    if (owns(box, "loaded_slot")) loaded = box.loaded_slot;
    else if (owns(extras, "loaded_slot")) loaded = extras.loaded_slot;
    // An explicit cleared status must not revive the saved previous slot.
    if (loaded !== "slot-1" && slotNumber(loaded) === undefined) loaded = "";
    const lastLoaded = slotNumber(loaded) ?? legacy.lastLoadSlot;
    return {...legacy, boxCount, slot: slots, slotSync: loaded, lastLoadSlot: lastLoaded,
      modernRecords: records, modernMaterials};
  }

  function items(variables, legacy) {
    const result = legacy.map(item => ({...item}));
    for (let index = 0; index < 17; index++) {
      const material = variables.modernRecords[index];
      if (!material) continue;
      const present = index === 16 || variables.slot[index] === 1;
      result[index] = {...result[index],
        color: present ? color(material.color_rgb_str) || "#00000000" : "#00000000",
        filament: present ? text(material.filament_str) || text(material.filament_type) : "",
        vendor: present ? text(material.vendor_str) : ""};
    }
    return result;
  }

  function options(dictionary, kind, current) {
    const values = new Set();
    if (kind === "filament") {
      for (const [key, item] of Object.entries(dictionary || {}))
        if (key.startsWith("fila") && typeof item?.filament === "string") values.add(item.filament);
    } else {
      const legacy = dictionary?.[kind === "vendor" ? "vendor_list" : "colordict"] || {};
      for (const value of Object.values(legacy)) if (typeof value === "string") values.add(value);
    }
    for (const item of current) if (typeof item?.[kind] === "string" && item[kind]) values.add(item[kind]);
    return values.size ? Array.from(values) : [""];
  }
  const numeric = value => value !== null && value !== undefined && value !== "" && Number.isFinite(Number(value))
    ? Number(value) : undefined;

  function profileLimit(status, boxNumber, legacy, dictionary) {
    if (!Number.isInteger(boxNumber) || boxNumber < 1 || boxNumber > 4) return null;
    const model = variables(status, legacy || {}), limits = [];
    for (let index = (boxNumber - 1) * 4; index < boxNumber * 4; index++) {
      if (model.slot[index] !== 1) continue;
      const material = model.modernRecords[index] || dictionary?.["fila" + model.filamentSlot?.[index]];
      const limit = numeric(material?.box_max_temp);
      if (limit !== undefined && limit >= 0) limits.push(limit);
    }
    return limits.length ? Math.min(...limits) : null;
  }

  function heaterSettings(status, name, original, legacy, dictionary) {
    const match = /^heater_generic heater_box([1-4])$/.exec(name);
    if (!match) return original;
    const number = Number(match[1]);
    const generated = status.configfile?.settings?.[`box_config box${number - 1}`]
      || status.configfile?.config?.[`box_config box${number - 1}`] || {};
    const setting = key => numeric(original?.[key]) ?? numeric(generated[key + "_heater_generic"]);
    // The Box is rated for 65 C. Respect any lower configured heater/target limit.
    // Unknown firmware bounds permit off only; never invent a higher limit.
    const max = Math.max(0, Math.min(65, setting("max_temp") ?? 0));
    const targetMax = Math.max(0, Math.min(max, setting("target_max_temp") ?? max));
    const materialMax = profileLimit(status, number, legacy, dictionary);
    return {...(original || {}), min_temp: Math.max(0, setting("min_temp") ?? 0), max_temp: max,
      target_min_temp: Math.max(0, setting("target_min_temp") ?? 0), target_max_temp: targetMax,
      material_max_temp: materialMax,
      temperature_hint: `Manual target: 0-${targetMax} C.` + (materialMax === null ? "" : ` Material profile maximum: ${materialMax} C.`)};
  }
  return {variables, items, options, heaterSettings, profileLimit};
})();
if (typeof module !== "undefined" && module.exports) module.exports = QidiBoxWebStatus;
