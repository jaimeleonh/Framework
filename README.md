# HH -> bbtautau Framework

## How to install
```sh
git clone --recursive git@github.com:cms-hh-bbtautau/Framework.git
```

## Loading environment
Following command activates the framework environment:
```sh
source env.sh
```
## How to run miniAOD->nanoAOD skims production

1. Load environment on CentOS8 machine
   ```sh
   source env.sh
   source /cvmfs/cms.cern.ch/common/crab-setup.sh
   voms-proxy-init -voms cms -rfc -valid 192:00
   ```

1. Create crab configs
   ```sh
   python3 NanoProd/createCrabConfigs.py --samples config/samples_2018.yaml --output crab/Run2_2018
   ```

1. Modify output and other site-specific settings in `config/overseer_cfg.yaml`. In particular:
   - site
   - crabOutput
   - localCrabOutput
   - finalOutput
   - renewKerberosTicket

1. Try that the code works locally (take one of the miniAOD files as an input). E.g.
   ```sh
   python3 RunKit/nanoProdWrapper.py customise=Framework/NanoProd/customiseNano.customise skimCfg=config/skim.yaml maxEvents=100 sampleType=mc storeFailed=True era=Run2_2018 inputFiles=file:/eos/cms/store/group/phys_tau/kandroso/miniAOD_UL18/TTToSemiLeptonic.root
   ./RunKit/nanoProdCrabJob.sh
   ```
   - check that output file `nano.root` is created correctly

1. Submit tasks using `RunKit/crabOverseer.py` and monitor the process.
   It is recommended to run `crabOverseer` in screen.
   ```sh
   python3 RunKit/crabOverseer.py --cfg config/overseer_cfg.yaml crab/Run2_2018/FILE1.yaml crab/Run2_2018/FILE2.yaml ...
   ```
   - Use `crab/Run2_2018/*.yaml` to submit all the tasks
   - For more information about available command line arguments run `python3 RunKit/crabOverseer.py --help`

## How to run nanoAOD->nanoAOD skims production
```sh
law run CreateNanoSkims --version prod_v1 --periods 2016,2016APV,2017,2018 --ignore-missing-samples True
```
## How to run HHbtag training skim ntuple production
```sh
python Studies/HHBTag/CreateTrainingSkim.py --inFile $CENTRAL_STORAGE/prod_v1/nanoAOD/2018/GluGluToBulkGravitonToHHTo2B2Tau_M-350.root --outFile output/skim.root --mass 350 --sample GluGluToBulkGraviton --year 2018 >& EventInfo.txt
python Common/SaveHisto.txt --inFile $CENTRAL_STORAGE/prod_v1/nanoAOD/2018/GluGluToBulkGravitonToHHTo2B2Tau_M-350.root --outFile output/skim.root
```

