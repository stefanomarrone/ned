#!/bin/bash

# Default values
MPAR_CHLOAD=1
MPAR_CHPARALLEL=1
RPAR_PFRAUD="9.0"
RPAR_RCH="0.000069"
RPAR_RENDCALL="0.001667"
RPAR_RFRAUD="0.01"
GREATSPN_SCRIPTS="/opt/greatspn/lib/app/portable_greatspn/bin/"
MODEL_NAME="Shared"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -chload) MPAR_CHLOAD="$2"; shift ;;
        -chparallel) MPAR_CHPARALLEL="$2"; shift ;;
        -pfraud) RPAR_PFRAUD="$2"; shift ;;
        -rch) RPAR_RCH="$2"; shift ;;
        -rendcall) RPAR_RENDCALL="$2"; shift ;;
        -rfraud) RPAR_RFRAUD="$2"; shift ;;
        -model) MODEL_NAME="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Run the commands with configurable values
"${GREATSPN_SCRIPTS}/WNRG" "${MODEL_NAME}" -mpar CHload "${MPAR_CHLOAD}" -mpar CHparallel "${MPAR_CHPARALLEL}" -rpar Pfraud "${RPAR_PFRAUD}" -rpar Rch "${RPAR_RCH}" -rpar Rendcall "${RPAR_RENDCALL}" -rpar Rfraud "${RPAR_RFRAUD}" -m -gui-stat -dot-F "${MODEL_NAME}-RG-0" -max-dot-markings 80

cp /dev/null "${MODEL_NAME}.gst"

"${GREATSPN_SCRIPTS}/swn_stndrd" "${MODEL_NAME}"

"${GREATSPN_SCRIPTS}/swn_ggsc" "${MODEL_NAME}" "-e1.0E-7" -i10000

cp "${MODEL_NAME}.epd" "${MODEL_NAME}.mpd"

"${GREATSPN_SCRIPTS}/swn_gst_prep" "${MODEL_NAME}" -mpar CHload "${MPAR_CHLOAD}" -mpar CHparallel "${MPAR_CHPARALLEL}" -rpar Pfraud "${RPAR_PFRAUD}" -rpar Rch "${RPAR_RCH}" -rpar Rendcall "${RPAR_RENDCALL}" -rpar Rfraud "${RPAR_RFRAUD}"

"${GREATSPN_SCRIPTS}/swn_gst_stndrd" "${MODEL_NAME}" -append "${MODEL_NAME}.sta"
