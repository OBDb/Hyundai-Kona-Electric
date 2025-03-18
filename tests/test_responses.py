import glob
import os
import pytest
from pathlib import Path
from typing import Dict, Any

# These will be imported from the schemas repository
from schemas.python.can_frame import CANIDFormat
from schemas.python.json_formatter import format_file
from schemas.python.signals_testing import obd_testrunner_by_year

REPO_ROOT = Path(__file__).parent.parent.absolute()

TEST_CASES = [
    {
        "model_year": 2023,
        "tests": [
            # Tire pressure
            ("""
7A8101762C00BFFFF00
7A82100B6490100B748
7A8220100B6480100B7
7A823480100AAAAAAAA
""", {
    "KONAEV_TP_FL": 36.4,
    "KONAEV_TT_FL": 23,
    "KONAEV_TP_FR": 36.6,
    "KONAEV_TT_FR": 22,
    "KONAEV_TP_RL": 36.4,
    "KONAEV_TT_RL": 22,
    "KONAEV_TP_RR": 36.6,
    "KONAEV_TT_RR": 22,
    }),
            ("""
7A8101762C00BFFFF00
7A82100B7490100B749
7A8220100B7490100B7
7A823480100AAAAAAAA
""", {
    "KONAEV_TP_FL": 36.6,
    "KONAEV_TT_FL": 23,
    "KONAEV_TP_FR": 36.6,
    "KONAEV_TT_FR": 23,
    "KONAEV_TP_RL": 36.6,
    "KONAEV_TT_RL": 23,
    "KONAEV_TP_RR": 36.6,
    "KONAEV_TT_RR": 22,
    }),

            # Speed
            ("""
7EA10186101FFF80000
7EA2109285A7611D908
7EA229853B4018C7734
7EA2304080805000000
""", {
    "KONAEV_VSS": 44.7,
    }),
            ("""
7EA10186101FFF80000
7EA2109285AA90DE006
7EA22DA33BE06997734
7EA2304080805000000
""", {
    "KONAEV_VSS": 34.97,
    }),

            # Battery state
            ("""
7EC103E620101FFF7E7
7EC21FF820000000003
7EC2200780EA8151515
7EC23151515000015BF
7EC240BBF4100008A00
7EC2501A09F00019C65
7EC26000097E6000093
7EC276B011C17660D01
7EC2876033803380BB8
""", {
    "KONAEV_HVBAT_SOC": 65,
    "KONAEV_HVBAT_CHARGING": 0,
    "KONAEV_HVBAT_PLUG_RAPD": 0,
    "KONAEV_HVBAT_PLUG_NORM": 0,
    "KONAEV_HVBAT_CURR": 12,
    "KONAEV_HVBAT_VDC": 375.2,
    "KONAEV_HVBAT_T_MAX": 21,
    "KONAEV_HVBAT_T_MIN": 21,
    "KONAEV_HVBAT_MOD1_T": 21,
    "KONAEV_HVBAT_MOD2_T": 21,
    "KONAEV_HVBAT_MOD3_T": 21,
    "KONAEV_HVBAT_MOD4_T": 21,
    "KONAEV_HVBAT_INLET_T": 21,
    "KONAEV_C_V_MAX": 3.82,
    "KONAEV_C_V_MAX_ID": 11.0,
    "KONAEV_C_V_MIN": 3.82,
    "KONAEV_C_V_MIN_ID": 65,
    "KONAEV_HVBAT_FAN_STATUS": 0,
    "KONAEV_HVBAT_FAN": 0,
    "KONAEV_VPWR": 13.8,
    "KONAEV_HVBAT_CHRG_TOT_C": 10665.5,
    "KONAEV_HVBAT_DSCH_TOT_C": 10557.3,
    "KONAEV_HVBAT_CHRG_TOT_E": 3888.6,
    "KONAEV_HVBAT_DSCH_TOT_E": 3773.9,
    "KONAEV_DRIVE_TIME": 18618214.0,
    "KONAEV_IGN": 1,
    "KONAEV_INVRT_CV": 374.0,
    "KONAEV_RPM": 824.0,
    "KONAEV_ISO_R": 3000.0,
    }),
            ("""
7EC103E620101FFF7E7
7EC21FF760000000003
7EC2202750E2B161515
7EC23151516000016B9
7EC240AB84100009200
7EC2501A0C900019D07
7EC26000097F5000093
7EC27A6011C237B0D01
7EC28680E990E990BB8
""", {
    "KONAEV_HVBAT_SOC": 59,
    "KONAEV_HVBAT_CHARGING": 0,
    "KONAEV_HVBAT_PLUG_RAPD": 0,
    "KONAEV_HVBAT_PLUG_NORM": 0,
    "KONAEV_HVBAT_CURR": 62.9,
    "KONAEV_HVBAT_VDC": 362.7,
    "KONAEV_HVBAT_T_MAX": 22,
    "KONAEV_HVBAT_T_MIN": 21,
    "KONAEV_HVBAT_MOD1_T": 21,
    "KONAEV_HVBAT_MOD2_T": 21,
    "KONAEV_HVBAT_MOD3_T": 21,
    "KONAEV_HVBAT_MOD4_T": 22,
    "KONAEV_HVBAT_INLET_T": 22,
    "KONAEV_C_V_MAX": 3.7,
    "KONAEV_C_V_MAX_ID": 10.0,
    "KONAEV_C_V_MIN": 3.68,
    "KONAEV_C_V_MIN_ID": 65,
    "KONAEV_HVBAT_FAN_STATUS": 0,
    "KONAEV_HVBAT_FAN": 0,
    "KONAEV_VPWR": 14.6,
    "KONAEV_HVBAT_CHRG_TOT_C": 10669.7,
    "KONAEV_HVBAT_DSCH_TOT_C": 10573.5,
    "KONAEV_HVBAT_CHRG_TOT_E": 3890.1,
    "KONAEV_HVBAT_DSCH_TOT_E": 3779.8,
    "KONAEV_DRIVE_TIME": 18621307.0,
    "KONAEV_IGN": 1,
    "KONAEV_INVRT_CV": 360.0,
    "KONAEV_RPM": 3737.0,
    "KONAEV_ISO_R": 3000,
    }),
        ]
    },
]

@pytest.mark.parametrize(
    "test_group",
    TEST_CASES,
    ids=lambda test_case: f"MY{test_case['model_year']}"
)
def test_signals(test_group: Dict[str, Any]):
    """Test signal decoding against known responses."""
    # Run each test case in the group
    for response_hex, expected_values in test_group["tests"]:
        try:
            obd_testrunner_by_year(
                test_group['model_year'],
                response_hex,
                expected_values,
                can_id_format=CANIDFormat.ELEVEN_BIT
            )
        except Exception as e:
            pytest.fail(
                f"Failed on response {response_hex} "
                f"(Model Year: {test_group['model_year']}: {e}"
            )

def get_json_files():
    """Get all JSON files from the signalsets/v3 directory."""
    signalsets_path = os.path.join(REPO_ROOT, 'signalsets', 'v3')
    json_files = glob.glob(os.path.join(signalsets_path, '*.json'))
    # Convert full paths to relative filenames
    return [os.path.basename(f) for f in json_files]

@pytest.mark.parametrize("test_file",
    get_json_files(),
    ids=lambda x: x.split('.')[0].replace('-', '_')  # Create readable test IDs
)
def test_formatting(test_file):
    """Test signal set formatting for all vehicle models in signalsets/v3/."""
    signalset_path = os.path.join(REPO_ROOT, 'signalsets', 'v3', test_file)

    formatted = format_file(signalset_path)

    with open(signalset_path) as f:
        assert f.read() == formatted

if __name__ == '__main__':
    pytest.main([__file__])
