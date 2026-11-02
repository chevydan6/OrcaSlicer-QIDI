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
 static void append_box_status(const nlohmann::json&, nlohmann::json&);
 static void append_chamber_status(const nlohmann::json&, nlohmann::json&);
 static std::string build_tool_slot_script(const std::string&);
 static std::string build_box_selection_script(const PrintParams&);
};
'''
for start,end in functions:
 code += source[source.index(start):source.index(end,source.index(start))]
code += r'''
int main() {
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
 assert(QidiPrinterAgent::build_box_selection_script({false,"[3]",false,false,{}}) == "SAVE_VARIABLE VARIABLE=enable_box VALUE=0");
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
 params.extra_options = R"({"qidi":{"is_support_multi_box":true,"qidi_preprint_bed_leveling":true,"is_support_timelapse":true}})";
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
