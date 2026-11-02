#!/usr/bin/env python3
"""Compile selected production helper bodies in isolation; NOT a slicer build."""
from pathlib import Path
import subprocess
root = Path(__file__).resolve().parents[1]
source = (root/'OrcaSlicer/src/slic3r/Utils/QidiPrinterAgent.cpp').read_text()
functions = [
 ('std::optional<std::string> QidiPrinterAgent::control_script', 'int QidiPrinterAgent::command_ams_refresh_rfid'),
 ('void QidiPrinterAgent::append_chamber_status', 'AgentInfo QidiPrinterAgent::get_agent_info_static'),
 ('std::string QidiPrinterAgent::build_tool_slot_script', 'std::string QidiPrinterAgent::build_box_selection_script'),
 ('std::string QidiPrinterAgent::build_box_selection_script', 'bool QidiPrinterAgent::print_uploaded_file'),
]
code = '''#include <nlohmann/json.hpp>
#include <optional>
#include <stdexcept>
#include <string>
#include <cassert>
struct PrintParams { bool task_use_ams{}; std::string ams_mapping; };
struct QidiPrinterAgent {
 static std::optional<std::string> control_script(const nlohmann::json&);
 static void append_chamber_status(const nlohmann::json&, nlohmann::json&);
 static std::string build_tool_slot_script(const std::string&);
 static std::string build_box_selection_script(const PrintParams&);
};
'''
for start,end in functions:
 code += source[source.index(start):source.index(end,source.index(start))]
code += r'''
int main() {
 assert(QidiPrinterAgent::build_tool_slot_script("[-1,-1,5]") == "SAVE_VARIABLE VARIABLE=value_t2 VALUE=\"'slot5'\"");
 assert(QidiPrinterAgent::build_tool_slot_script("[3,-1,0]") == "SAVE_VARIABLE VARIABLE=value_t0 VALUE=\"'slot3'\"\nSAVE_VARIABLE VARIABLE=value_t2 VALUE=\"'slot0'\"");
 assert(QidiPrinterAgent::build_tool_slot_script("[16]").empty());
 assert(QidiPrinterAgent::build_box_selection_script({false,"[3]"}) == "SAVE_VARIABLE VARIABLE=enable_box VALUE=0");
 assert(QidiPrinterAgent::build_box_selection_script({true,"[]"}).empty());
 assert(QidiPrinterAgent::control_script({{"command","set_ctt"},{"ctt_val",45}}) == "SET_HEATER_TEMPERATURE HEATER=chamber TARGET=45");
 assert(QidiPrinterAgent::control_script({{"command","ams_get_rfid"},{"ams_id",3},{"slot_id",3}}) == "READ_RFID SLOT=15");
 assert(QidiPrinterAgent::control_script({{"command","ams_change_filament"},{"ams_id",1},{"slot_id",2},{"target",255}}) == "UNLOAD_FILAMENT_CONTROL SLOT=6");
 bool rejected=false;
 try { QidiPrinterAgent::control_script({{"command","set_ctt"},{"ctt_val",66}}); }
 catch(const std::invalid_argument&) { rejected=true; }
 assert(rejected);
 nlohmann::json payload;
 QidiPrinterAgent::append_chamber_status({{"heater_generic chamber",{{"temperature",42.5},{"target",55}}}},payload);
 assert(payload["print"]["chamber_temper"]==42.5);
 assert(payload["print"]["ctt"]==55);
}
'''
build = root/'build/protocol-helpers'
build.mkdir(parents=True,exist_ok=True)
(build/'test.cpp').write_text(code)
subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-Werror','-I'+str(root/'OrcaSlicer/deps_src'),str(build/'test.cpp'),'-o',str(build/'test')],check=True)
subprocess.run([str(build/'test')],check=True)
print('PASS: isolated production protocol helper compilation and offline assertions. Full app compilation, GUI, HTTP and hardware are NOT covered.')
