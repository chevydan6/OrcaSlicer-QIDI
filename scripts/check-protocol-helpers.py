#!/usr/bin/env python3
"""Compile selected production helper bodies in isolation; NOT a slicer build."""
from pathlib import Path
import subprocess
root = Path(__file__).resolve().parents[1]
source = (root/'OrcaSlicer/src/slic3r/Utils/QidiPrinterAgent.cpp').read_text()
functions = [
 ('std::optional<std::string> QidiPrinterAgent::control_script', 'int QidiPrinterAgent::command_ams_refresh_rfid'),
 ('void QidiPrinterAgent::append_chamber_status', 'AgentInfo QidiPrinterAgent::get_agent_info_static'),
 ('void QidiPrinterAgent::append_accessory_status', 'nlohmann::json QidiPrinterAgent::configuration_notification'),
 ('nlohmann::json QidiPrinterAgent::configuration_notification', 'void QidiPrinterAgent::append_box_status'),
 ('void QidiPrinterAgent::append_box_status', 'std::string QidiPrinterAgent::camera_url_for_host'),
 ('std::string QidiPrinterAgent::camera_url_for_host', 'std::string QidiPrinterAgent::get_camera_url'),
 ('std::string QidiPrinterAgent::build_tool_slot_script', 'std::string QidiPrinterAgent::build_box_selection_script'),
 ('std::string QidiPrinterAgent::build_box_selection_script', 'bool QidiPrinterAgent::print_uploaded_file'),
 ('bool QidiPrinterAgent::print_uploaded_file', 'bool QidiPrinterAgent::set_timelapse_enabled'),
]
code = '''#include <nlohmann/json.hpp>
#include <optional>
#include <stdexcept>
#include <string>
#include <cassert>
#include <algorithm>
#include <cctype>
#include <vector>
#include <sstream>
#include <ios>
#include <utility>
struct PrintParams {
 bool task_use_ams{}; std::string ams_mapping;
 bool task_bed_leveling{}, task_record_timelapse{};
 std::string extra_options;
};
struct QidiPrinterAgent {
 struct { std::string dev_id, base_url, api_key; } device_info;
 std::vector<std::string> calls;
 unsigned fail_at = 0;
 bool record(const std::string& call) { calls.push_back(call); return calls.size() != fail_at; }
 bool send_gcode_sync(const std::string&, const std::string& script) { return record(script); }
 bool set_timelapse_enabled(bool enabled) { return record(enabled ? "timelapse:on" : "timelapse:off"); }
 static nlohmann::json print_start_request(const PrintParams&, const std::string& filename) { return {{"filename",filename}}; }
 bool send_jsonrpc_command(const std::string&, const std::string&, const nlohmann::json& request, std::string&)
 { return record("start:" + request["filename"].get<std::string>()); }
 bool print_uploaded_file(const PrintParams&, const std::string&);
 static std::optional<std::string> control_script(const nlohmann::json&);
 static std::string camera_url_for_host(std::string);
 static nlohmann::json configuration_notification(const nlohmann::json&);
 static void append_accessory_status(const nlohmann::json&, nlohmann::json&);
 static std::optional<int> reported_box_count(const nlohmann::json&, bool legacy_default = false);
 static nlohmann::json decoded_box_slot(const nlohmann::json&, int);
 static void append_box_status(const nlohmann::json&, nlohmann::json&);
 static void append_chamber_status(const nlohmann::json&, nlohmann::json&);
 static std::string build_tool_slot_script(const std::string&);
 static std::string build_box_selection_script(const PrintParams&);
};
'''
for start,end in functions:
 code += source[source.index(start):source.index(end,source.index(start))]
cache_source = (root/'OrcaSlicer/src/slic3r/Utils/MoonrakerPrinterAgent.cpp').read_text()
qidi_header = (root/'OrcaSlicer/src/slic3r/Utils/QidiPrinterAgent.hpp').read_text()
code += """
#include <mutex>
struct MoonrakerCacheHarness {
 std::recursive_mutex payload_mutex;
 nlohmann::json status_cache;
 virtual bool merge_status_object_recursively(const std::string&) const { return false; }
 void update_status_cache(const nlohmann::json&);
};
struct QidiCacheHarness : MoonrakerCacheHarness {
"""
start=qidi_header.index('    bool merge_status_object_recursively')
code += qidi_header[start:qidi_header.index('    void append_status_payload',start)] + '};\n'
start=cache_source.index('void MoonrakerPrinterAgent::update_status_cache')
code += cache_source[start:cache_source.index('nlohmann::json MoonrakerPrinterAgent::build_print_payload_locked',start)].replace('MoonrakerPrinterAgent::','MoonrakerCacheHarness::')
gui_source = (root/'OrcaSlicer/src/slic3r/GUI/DeviceCore/DevFilaSystem.cpp').read_text()
code += """
struct DevAmsTray {
 int hold_count=0, ctype=0;
 bool is_exists=false, is_slot_placeholder=false;
 std::string setting_id, m_fila_type, sub_brands, color;
 std::vector<std::string> cols;
 void UpdateColorFromStr(const std::string& value) { color=value; }
};
struct DevFilaSystemParser {
 static void UpdateQidiTray(DevAmsTray&,const nlohmann::json&,const std::string&);
};
"""
start=gui_source.index('void DevFilaSystemParser::UpdateQidiTray')
code += gui_source[start:gui_source.index('void DevFilaSystemParser::ParseV1_0',start)]
code += r'''
int main() {
 const nlohmann::json first{{"multi_color_controller",{{"box",{{"box_count",2},{"box1_filament_info_2_filament_type","PETG"}}}}}};
 const nlohmann::json second{{"multi_color_controller",{{"box",{{"box1_aht20_temp",32.5}}}}}};
 QidiCacheHarness cache;
 cache.update_status_cache(first);cache.update_status_cache(second);
 assert(QidiPrinterAgent::reported_box_count(cache.status_cache)==2);
 assert(QidiPrinterAgent::decoded_box_slot(cache.status_cache,6)["filament_type"]=="PETG");
 MoonrakerCacheHarness ordinary_cache;
 ordinary_cache.update_status_cache(first);ordinary_cache.update_status_cache(second);
 assert(!ordinary_cache.status_cache["multi_color_controller"]["box"].contains("box_count"));

 assert(QidiPrinterAgent::camera_url_for_host("http://127.0.0.1:7125/")=="http://127.0.0.1/webcam/?action=snapshot");

 nlohmann::json external;
 QidiPrinterAgent::append_box_status({{"multi_color_controller",{{"extra",{{"filament_info",{{"filament_type","PLA"},{"color_rgb_str",{"112233"}}}}}}}}},external);
 assert(external["print"]["qidi_external_slot"]["color"]=="112233");
 assert(!external["print"].contains("ams"));

 assert(QidiPrinterAgent::control_script({{"command","qidi_exclude_objects"},{"objects",{"cube_id_5_copy_0"}}})=="EXCLUDE_OBJECT NAME=cube_id_5_copy_0");
 nlohmann::json object_status;
 QidiPrinterAgent::append_accessory_status({{"exclude_object",{{"objects",{{{"name","cube"}},{{"name","tower"}}}},{"excluded_objects",{"tower"}}}}},object_status);
 assert(object_status["print"]["qidi_print_objects"]==nlohmann::json::array({"cube"}));

 assert(QidiPrinterAgent::build_tool_slot_script("[3,4294967296]").empty());
 assert(QidiPrinterAgent::build_tool_slot_script("[3,16]").empty());
 assert(QidiPrinterAgent::build_tool_slot_script("[3,true]").empty());
 PrintParams incomplete;
 incomplete.task_use_ams=true;incomplete.ams_mapping="[3,-1,-1]";
 incomplete.extra_options=R"({"qidi":{"is_support_multi_box":true,"used_filaments":[0,2]}})";
 QidiPrinterAgent stopped;
 assert(!stopped.print_uploaded_file(incomplete,"do-not-start.gcode") && stopped.calls.empty());
 incomplete.ams_mapping="[15,-1,4]";
 assert(QidiPrinterAgent::build_box_selection_script(incomplete)=="SAVE_VARIABLE VARIABLE=enable_box VALUE=1\nSAVE_VARIABLE VARIABLE=value_t0 VALUE=\"'slot15'\"\nSAVE_VARIABLE VARIABLE=value_t2 VALUE=\"'slot4'\"");
 incomplete.task_use_ams=false;
 assert(QidiPrinterAgent::build_box_selection_script(incomplete).empty());

 DevAmsTray tray;
 tray.setting_id="specific-PLA";tray.m_fila_type="PLA";tray.color="112233FF";tray.is_exists=true;
 DevFilaSystemParser::UpdateQidiTray(tray,{{"filament_type","PLA"},{"present",true}},"generic-PLA");
 assert(tray.setting_id=="specific-PLA" && tray.color=="112233FF");
 DevFilaSystemParser::UpdateQidiTray(tray,{{"filament_type","PETG"},{"color","#ABCDEF"}},"PETG");
 assert(tray.setting_id=="PETG" && tray.color=="ABCDEFFF");
 DevFilaSystemParser::UpdateQidiTray(tray,{{"present",false},{"color","bad-color"}},"");
 assert(!tray.is_exists && tray.is_slot_placeholder && tray.setting_id=="PETG" && tray.color=="ABCDEFFF");
 tray.hold_count=1;
 DevFilaSystemParser::UpdateQidiTray(tray,{{"present",true}},"");
 assert(!tray.is_exists);
 DevFilaSystemParser::UpdateQidiTray(tray,{{"present",true},{"filament_type","unknown"}},"");
 assert(tray.is_exists && tray.is_slot_placeholder && tray.setting_id.empty());

 assert(QidiPrinterAgent::reported_box_count({},true)==1);
 assert(!QidiPrinterAgent::reported_box_count({{"multi_color_controller",{{"box_count",4294967296ULL}}}},true));
 assert(QidiPrinterAgent::decoded_box_slot({{"multi_color_controller",{{"box1_box_inserted_2",1},{"box1_filament_info_2_filament_type","PETG"},{"box1_filament_info_2_color_rgb_str",{"AABBCC","DDEEFF"}}}}},6)["color"]=="AABBCC");
 nlohmann::json loaded;
 QidiPrinterAgent::append_box_status({{"multi_color_controller",{{"last_load_slot","slot15"}}}},loaded);
 assert(loaded["print"]["ams"]["tray_now"]=="15");

 assert(QidiPrinterAgent::control_script({{"command","qidi_polar_cooler"},{"enabled",false}}) == "SET_PIN PIN=polar_cooler VALUE=0");
 nlohmann::json detector_payload;
 QidiPrinterAgent::append_accessory_status({{"save_variables",{{"variables",{{"enable_noodle_detection",1},{"enable_pre_print_model_check",false},{"noodle_sensitivity_level","MEDIUM"}}}}},{"output_pin polar_cooler",{{"value",1}}}},detector_payload);
 assert(detector_payload["print"]["qidi_detection"]["enable_noodle_detection"] == true);
 assert(detector_payload["print"]["qidi_detection"]["sensitivity"] == "medium");
 assert(detector_payload["print"]["qidi_polar_cooler_on"] == true);
 assert(QidiPrinterAgent::control_script({{"command","xcam_control_set"},{"module_name","fod_check"},{"control",true}}) == "SAVE_VARIABLE VARIABLE=enable_pre_print_model_check VALUE=1");
 assert(QidiPrinterAgent::control_script({{"command","xcam_control_set"},{"module_name","spaghetti_detector"},{"control",false},{"halt_print_sensitivity","high"}}) == "SAVE_VARIABLE VARIABLE=enable_noodle_detection VALUE=0\nSAVE_VARIABLE VARIABLE=noodle_sensitivity_level VALUE=\"'HIGH'\"");
 assert(QidiPrinterAgent::build_tool_slot_script("[-1,-1,5]") == "SAVE_VARIABLE VARIABLE=value_t2 VALUE=\"'slot5'\"");
 assert(QidiPrinterAgent::build_tool_slot_script("[3,-1,0]") == "SAVE_VARIABLE VARIABLE=value_t0 VALUE=\"'slot3'\"\nSAVE_VARIABLE VARIABLE=value_t2 VALUE=\"'slot0'\"");
 assert(QidiPrinterAgent::build_tool_slot_script("[16]").empty());
 assert(QidiPrinterAgent::build_box_selection_script({false,"[-1]",false,false,R"({"qidi":{"used_filaments":[0]}})"}) == "SAVE_VARIABLE VARIABLE=enable_box VALUE=0");
 assert(QidiPrinterAgent::build_box_selection_script({true,"[]",false,false,{}}).empty());
 assert(QidiPrinterAgent::control_script({{"command","set_ctt"},{"ctt_val",45}}) == "SET_HEATER_TEMPERATURE HEATER=chamber TARGET=45");
 assert(QidiPrinterAgent::control_script({{"command","ams_get_rfid"},{"ams_id",3},{"slot_id",3}}) == "READ_RFID SLOT=15");
 assert(QidiPrinterAgent::control_script({{"command","ams_change_filament"},{"ams_id",1},{"slot_id",2},{"target",255}}) == "UNLOAD_FILAMENT_CONTROL SLOT=6");
 assert(QidiPrinterAgent::control_script({{"command","ams_filament_setting"},{"ams_id",1},{"slot_id",3},{"tray_color","FF8000FF"},{"tray_vendor","QIDI"},{"tray_type","PLA"}}) == "UPDATE_FILAMENT_INFORMATION SLOT=7 COLOR='FF8000' VENDOR='QIDI' FILAMENT='PLA'");
 assert(QidiPrinterAgent::control_script({{"command","ams_eject_filament"},{"ams_id",2},{"slot_id",0}}) == "EJECT_FILAMENT_CONTROL SLOT=8");
 bool rejected=false;
 try { QidiPrinterAgent::control_script({{"command","set_ctt"},{"ctt_val",66}}); }
 catch(const std::invalid_argument&) { rejected=true; }
 assert(rejected);
 nlohmann::json payload;
 QidiPrinterAgent::append_chamber_status({{"heater_generic chamber",{{"temperature",42.5},{"target",55}}}},payload);
 assert(payload["print"]["chamber_temper"]==42.5);
 assert(payload["print"]["ctt"]==55);
 payload = nlohmann::json::object();
 QidiPrinterAgent::append_box_status({{"multi_color_controller",{{"box_count",2},{"box",{{"box0_aht20_temp",23.5},{"box1_aht20_humidity",35}}}}}},payload);
 assert(payload["print"]["ams"]["ams"].size()==2);
 assert(payload["print"]["ams"]["ams"][0]["temp"]=="23.5");
 assert(payload["print"]["ams"]["ams"][1]["humidity_raw"]=="35");
 assert(!payload["print"]["ams"]["ams"][0].contains("tray"));
 payload = nlohmann::json::object();
 QidiPrinterAgent::append_box_status({{"multi_color_controller",{{"box_count",4294967296ULL}}}},payload);
 assert(payload.empty());
 payload = {{"print", {{"fan_gear",64}}}};
 QidiPrinterAgent::append_accessory_status({{"output_pin caselight",{{"value",1}}},{"fan_generic auxiliary_cooling_fan",{{"speed",0.5}}},{"fan_generic chamber_circulation_fan",{{"speed",1.0}}}},payload);
 assert(payload["print"]["fan_gear"] == (64U | (128U << 8) | (255U << 16)));
 assert(payload["print"]["lights_report"][0]["mode"] == "on");
 assert(QidiPrinterAgent::control_script({{"command","ledctrl"},{"led_node","chamber_light"},{"led_mode","on"}}) == "SET_PIN PIN=caselight VALUE=1");
 const auto config = QidiPrinterAgent::configuration_notification({{"method","notify_proc_stat_update"},{"params",nlohmann::json::array({{{"config_items",{{"printing.polar_cooler","1"}}}}})}});
 assert(config["qidi_config"]["polar_cooler_available"] == true);
 assert(QidiPrinterAgent::camera_url_for_host("http://127.0.0.1:7125") == "http://127.0.0.1/webcam/?action=snapshot");
 assert(QidiPrinterAgent::camera_url_for_host("https://[::1]:8443") == "https://[::1]:8443/webcam/?action=snapshot");
 assert(QidiPrinterAgent::control_script({{"command","qidi_set_fan"},{"fan_index",1},{"speed",255}}) == "SET_FAN_SPEED FAN=cooling_fan SPEED=1.0");
 assert(QidiPrinterAgent::control_script({{"command","print_speed"},{"param","3"}}) == "M220 S124");
 PrintParams params;
 params.task_use_ams = true;
 params.ams_mapping = "[-1,-1,5]";
 params.task_bed_leveling = true;
 params.task_record_timelapse = true;
 params.extra_options = R"({"qidi":{"is_support_multi_box":true,"used_filaments":[2],"qidi_preprint_bed_leveling":true,"is_support_timelapse":true}})";
 QidiPrinterAgent agent;
 assert(agent.print_uploaded_file(params,"chosen.gcode.3mf"));
 assert(agent.calls.size() == 4);
 assert(agent.calls[0] == "SAVE_VARIABLE VARIABLE=enable_box VALUE=1\nSAVE_VARIABLE VARIABLE=value_t2 VALUE=\"'slot5'\"");
 assert(agent.calls[1] == "G31");
 assert(agent.calls[2] == "timelapse:on");
 assert(agent.calls[3] == "start:chosen.gcode.3mf");
 for (unsigned failure = 1; failure <= 3; ++failure) {
   agent.calls.clear(); agent.fail_at = failure;
   assert(!agent.print_uploaded_file(params,"must-not-start.gcode"));
   assert(agent.calls.size() == failure);
   for (const auto& call : agent.calls) assert(call.find("start:") != 0);
 }
 agent.calls.clear(); agent.fail_at = 0;
 auto extras = nlohmann::json::parse(params.extra_options);
 extras["qidi"]["polar_cooler"] = true;
 params.extra_options = extras.dump();
 assert(agent.print_uploaded_file(params,"cooler.gcode"));
 assert(agent.calls.size() == 5);
 assert(agent.calls[3] == "SAVE_VARIABLE VARIABLE=enable_polar_cooler VALUE=1");
 assert(agent.calls[4] == "start:cooler.gcode");
 agent.calls.clear(); params.ams_mapping = "[]";
 assert(!agent.print_uploaded_file(params,"must-not-start.gcode"));
 assert(agent.calls.empty());
}
'''
build = root/'build/protocol-helpers'
build.mkdir(parents=True,exist_ok=True)
(build/'test.cpp').write_text(code)
subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-Werror','-I'+str(root/'OrcaSlicer/deps_src'),str(build/'test.cpp'),'-o',str(build/'test')],check=True)
subprocess.run([str(build/'test')],check=True)
print('PASS: isolated production protocol helper compilation and offline assertions. Submission ordering and stop-on-failure use recording transports. Full app compilation, GUI, real HTTP and hardware are NOT covered.')
