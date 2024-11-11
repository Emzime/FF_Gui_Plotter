#!/bin/bash
cd "$(dirname "$0")" || exit

if (( $# == 0 )); then
    echo "Please add one parameter for version"; exit 1
fi

version=${1}

deactivate 2>/dev/null
. ../venv/bin/activate


rm -r dist/ 2>/dev/null
python System_Auto_Standalone_Builder.py

cd dist || exit
mv 'French Farmer Gui' "FrenchFarmer_Gui_${version}_linux_standalone"
cd ..

python System_Auto_Folder_Builder.py
cd dist || exit
tar czfv "FrenchFarmer_Gui_${version}_linux.tar.gz" French\ Farmer\ Gui/

echo "Successfully built in dist/"
