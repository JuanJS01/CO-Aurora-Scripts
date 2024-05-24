import os

# Script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Relative path to the root directory
relative_root_dir = r"\Aurora\SectorFiles\Include\COnew\ATC_OPS_Only\Scripts"

# Abs path to the root directory
root_dir = os.path.join(script_dir, relative_root_dir)

# Dictionary with AP ICAOs and relative Aurora's filepath
icao_dict = {
    "ANDES_TERM.fix": {"ICAOs":{"SETU","SKIP"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\ANDES\NAVAIDS",},
    "BAQ_TERM.fix": {"ICAOs":{"SKBQ","SKBR","SKCB","SKCG","SKCV","SKCZ","SKFU","SKMG","SKMR","SKSM","SKSR","SKTL"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\BAQ\NAVAIDS",},
    "BGA_TERM.fix": {"ICAOs":{"SKBG","SKCM","SKEJ","SKLA","SKOC","SKPA","SKSG","SKSO","SKTJ"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\BGA\NAVAIDS",},
    "BOG_TERM.fix": {"ICAOs":{"SKBO","SKTI","SKQU","SKIB","SKGY","SKGI","SKMA","SKME"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\BOG\NAVAIDS",},
    "CLO_TERM.fix": {"ICAOs":{"SKBU","SKCL","SKGO","SKHA","SKPP","SKUL","SKGB"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\CLO\NAVAIDS",},
    "CUC_TERM.fix": {"ICAOs":{"SKCC","SKCN","SKSA","SKTM","SKUC","SVSA"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\CUC\NAVAIDS",},
    "EYP_TERM.fix": {"ICAOs":{"SKHC","SKMN","SKPZ","SKTD","SKYP","SQUJ"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\EYP\NAVAIDS",},
    "LET_TERM.fix": {"ICAOs":{"SBTT","SKLT","SPBC","SWII"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\LET\NAVAIDS",},
    "MDE_TERM.fix": {"ICAOs":{"SKAM","SKMD","SKOT","SKRG","SKSF","SKUR"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\MDE\NAVAIDS",},
    "MIL_TERM.fix": {"ICAOs":{"SKCV","SKPQ","SKTI","SKME","SKJC","SKGB","SKNA","SKTQ","SKUA","SKAP","SKMA"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\FIR\MIL\NAVAIDS",},
    "NVA_TERM.fix": {"ICAOs":{"SKGZ","SKNV"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\NVA\NAVAIDS",},
    "PEI_TERM.fix": {"ICAOs":{"SKAR", "SKGO", "SKMZ","SKPE"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\PEI\NAVAIDS",},
    "SPP_TERM.fix": {"ICAOs":{"SKSP", "SKPV"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\SPP\NAVAIDS",},
    "VVC_TERM.fix": {"ICAOs":{"SKVV", "SKAP", "SKPG"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\TMA\VVC\NAVAIDS",},
    "SKEC_TERM.fix": {"ICAOs":{"SKBC","SKVP","SKPB","SKMP","SKBC","SKRH","SKLM","SKMJ"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\FIR\SKEC\NAVAIDS",},
    "SKED_TERM.fix": {"ICAOs":{"SKBS","SKNQ","SKUI","SKCD","SKJC","SKGP","SKCO","SKPS","SKAC","SKMU","SKLP","SKPI","SKVG","SKAS","SKFL","SKTQ","SKLG","SKSV","SKNA","SKSJ","SKMF","SKCR","SKPD","SKUA","SKPC","SKOE"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\FIR\SKED\NAVAIDS",},
    "BND_SKED_SKEC_AD_TERM.fix": {"ICAOs":{"SKNC","SKOC","SKAG","SKTB"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\Common\NAVAIDS",},
    "BND_SKED_SKEC_TERM.fix": {"ICAOs":{"SKML","SKCU","SKEB","SKAD","SKTU","SKLC"}, "subfolder": r"\Aurora\SectorFiles\Include\COnew\Common\NAVAIDS",},
}

# Construct the path to the input file (FIX_ALL.fix) relative to the root_dir
# Change for a sub root folder where navdata is going to be set // // // // // // // //
input_file = os.path.join(root_dir, "FIX_ALL.fix")

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Error: The specified input file does not exist: {input_file}")
else:
    # Initialize data structure to hold filtered data for output files
    output_files = {key: [] for key in icao_dict}

    # R and process input file
    with open(input_file, "r") as file:
        for line in file:
            parts = line.split(";")
            if len(parts) < 5:  # Check if there are enough parts
                continue
            parameter_str = parts[3].strip()
            parameter = int(parameter_str.replace("(", "").replace(")", ""))
            notes = parts[-1].strip()
            # Filter lines based on the 4th variable and ICAO code
            if parameter == 1 and "//" in notes:
                icao_code = notes.split("//")[-1].strip()  # Extract ICAO code
                for output_file, icao_info in icao_dict.items():
                    if icao_code in icao_info["ICAOs"]:
                        output_files[output_file].append(line.strip())  # Add to correct output file

    # Write to output files in their respective subfolders
    for filename, lines in output_files.items():
        subfolder = icao_dict[filename]["subfolder"]
        full_path = os.path.join(script_dir, subfolder, filename)

        # Make sure the subfolder exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as file:
            for line in lines:
                file.write(f"{line}\n")

    print("Output files have been created and placed in their respective subfolders.")
