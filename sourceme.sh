#!/bin/sh

function print_help {
   echo "supported arguments:";
   echo "   -a    (or --all)                do everything needed to setup the ASCII ART GENERATOR";
   echo "   -d    (or --dev)                do everything needed to develop the ASCII ART GENERATOR";
   echo "   -h    (or --help)               prints this help";
}

# Default values
all=0;
dev=0;
create_venv=0;
stop=0;

# Loop index
index=0
for argument in $@
  do
    # Incrementing index
    index=`expr $index + 1`

    # The conditions
    case $argument in
      -a)                     all=1;;
      --all)                  all=1;;
      -d)                     dev=1;;
      --dev)                  dev=1;;
      -h)                     print_help
                              stop=1;;
      --help)                 print_help
                              stop=1;;
      -*)                     echo "unsupported argument <$argument> with argument <${arguments[index]}>";
                              print_help
                              stop=1 ;;
    esac
  done

if [ "$stop" = "0" ] ; then
   if [ "$all" = "1" ] ; then
      create_venv=1;
   fi

   # Setup environment variables
   # -------------------------------------------------------------------
   echo "########## SETUP ASCII ART GENERATOR ##########"
   # Extracting the project name from the repo name and converting it to uppercase
   export PRJROOT=${PWD}
   export PRJNAME=${PWD##*/}

   echo "   PRJROOT = $PRJROOT"
   echo "   PRJNAME = $PRJNAME"

   # Create and activate virtual env
   # -------------------------------------------------------------------
   if [ "$create_venv" = "1" ] ; then
      echo "   -- creating Python virtualenv"
      rm -rf venv
      python3 -m virtualenv venv
   fi

   source venv/bin/activate

   if [ -n "$_OLD_VIRTUAL_PS1" ] ; then
      export PS1="($(basename $PRJROOT))$_OLD_VIRTUAL_PS1"
   fi

   if [ "$create_venv" = "1" ] ; then
      echo "   -- install ASCII Art generator package"
      pip install . -q
   fi
   if [ "$dev" = "1" ] ; then
      echo "   -- install ASCII Art generator package in editable mode"
      pip install -e .[dev] -q
      echo "   -- install ASCII Art pre-commit hooks"
      pre-commit install
   fi

   cd $PRJROOT

   echo "########## SETUP DONE ##########"

fi
