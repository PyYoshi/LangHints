#!/bin/bash

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

SCRIPT_PATH=$(realpath $0)
ROOT_PATH=`dirname $SCRIPT_PATH`/..
SRC_PATH=$ROOT_PATH/src
WORKSPACE_ROOT_PATH=$ROOT_PATH/workspace

WORKSPACE_VIM_PATH=$WORKSPACE_ROOT_PATH/vim
WORKSPACE_VSCODE_PATH=$WORKSPACE_ROOT_PATH/vscode
WORKSPACE_MOZILLA_CENTRAL_PATH=$WORKSPACE_ROOT_PATH/mozilla-central
WORKSPACE_MOZILLA_L10N_CENTRAL_PATH=$WORKSPACE_ROOT_PATH/mozilla-l10n-central
WORKSPACCE_WORDPRESS_PATH=$WORKSPACE_ROOT_PATH/wordpress

if [ ! -d $WORKSPACE_ROOT_PATH ]; then
	mkdir $WORKSPACE_ROOT_PATH
fi

update_vim() {
	if [ ! -d $WORKSPACE_VIM_PATH ]; then
		cd $WORKSPACE_ROOT_PATH
		git clone https://github.com/vim/vim.git
	else
		cd $WORKSPACE_VIM_PATH
		git reset --hard HEAD
		git checkout master
		git pull
	fi
}

update_vscode() {
	if [ ! -d $WORKSPACE_VSCODE_PATH ]; then
		cd $WORKSPACE_ROOT_PATH
		git clone https://github.com/Microsoft/vscode.git
	else
		cd $WORKSPACE_VSCODE_PATH
		git reset --hard HEAD
		git checkout master
		git pull
	fi
}

update_mozilla_central() {
	if [ ! -d $WORKSPACE_MOZILLA_CENTRAL_PATH ]; then
		cd $WORKSPACE_ROOT_PATH
		hg clone http://hg.mozilla.org/mozilla-central/ mozilla-central
	else
		cd $WORKSPACE_MOZILLA_CENTRAL_PATH
		hg update --clean
	fi
}

update_mozilla_l10n_central() {
	declare -a mozillaL10nCentralLocals=(
		"ach" "af" "ak" "ar" "as" "ast"
		"be" "bg" "bn-BD" "bn-IN" "br" "bs"
		"ca" "cs" "cy" "da" "de" "el"
		"en-GB" "en-ZA" "eo" "es-AR" "es-CL" "es-ES"
		"es-MX" "et" "eu" "fa" "ff" "ff"
		"fi" "fr" "fy-NL" "ga-IE" "gd" "gl"
		"gu-IN" "he" "hi-IN" "hr" "hu" "hy-AM"
		"id" "is" "it" "ja" "ja-JP-mac" "ka"
		"kk" "km" "kn" "ko" "ku" "lg"
		"lij" "lt" "lv" "mai" "mk" "ml"
		"mn" "mr" "ms" "my" "nb-NO" "ne-NP"
		"nl" "nn-NO" "nr" "nso" "oc" "or"
		"pa-IN" "pl" "pt-BR" "pt-PT" "rm" "ro"
		"ru" "rw" "si" "sk" "sl" "son"
		"sq" "sr" "ss" "st" "sv-SE" "ta"
		"ta-LK" "te" "th" "tn" "tr" "ts"
		"uk" "ve" "vi" "wo" "xh" "zh-CN"
		"zh-TW" "zu"
	)  

	if [ ! -d $WORKSPACE_MOZILLA_L10N_CENTRAL_PATH ]; then
		mkdir $WORKSPACE_MOZILLA_L10N_CENTRAL_PATH
	fi

	for mozillaL10nCentralLocal in ${mozillaL10nCentralLocals[@]}; do
		if [ ! -d $WORKSPACE_MOZILLA_L10N_CENTRAL_PATH/${mozillaL10nCentralLocal} ]; then
			cd $WORKSPACE_MOZILLA_L10N_CENTRAL_PATH
			hg clone http://hg.mozilla.org/l10n-central/${mozillaL10nCentralLocal}/ ${mozillaL10nCentralLocal}
		else
			cd $WORKSPACE_MOZILLA_L10N_CENTRAL_PATH/${mozillaL10nCentralLocal}
			hg update --clean
		fi
	done
}

update_wordpress() {
	if [ ! -d $WORKSPACCE_WORDPRESS_PATH ]; then
		mkdir $WORKSPACCE_WORDPRESS_PATH
	fi
	python $SRC_PATH/dl_wordpress.py
}

update_vim
update_vscode
update_mozilla_central
update_mozilla_l10n_central
update_wordpress
