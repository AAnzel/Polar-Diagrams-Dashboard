# Polar-Diagrams-Dashboard
## Manuscript

This library is created for the following paper:

***"Placeholder"*** by Aleksandar Anžel, Zewen Yang, and Georges Hattab

Please cite the paper as:
```latex
Placeholder
```

---
Abstract:

> Placeholder

## Dependencies

The code is written in Python 3.11.8 and tested on Linux with the following libraries installed:

|Library|Version|
|---|---|
|numpy|1.26.4|
|pandas|2.2.1|
|scikit-learn|1.4.1.post1|
|polar_diagrams|1.2.0|
|plotly|5.19.0|
|dash|2.14.2|
|dash_bootstrap_components|1.5.0|
|dash-tools|1.12.0|
|gunicorn|21.2.0|


The dependencies can also be found in [requirements.txt](requirements.txt).

## Data
|Location|Description|
|---|---|
|[data/](data/)|contains all data sets used in the dashboard.
|[data/Case_Study_Climate/](data/Case_Study_Climate/)|contains the data set used in the case study "4.1. Climate Model Comparison" in the original paper [1].
|[data/Case_Study_Ecoli/](data/Case_Study_Ecoli/)|contains the data set used in the case study "4.2. Machine Learning Model Comparison" in the original paper.
|[data/Case_Study_Gaussian_Processes/](data/Case_Study_Gaussian_Processes/)|contains the data set used in the case study "4.3. Machine Learning Hyper-parameter Tuning" in the original paper.


**[1]** Notes on how to download climate data
* The script used for downloading the [data/Case_Study_Climate/](data/Case_Study_Climate/) was generated using the tutorial found here https://esgf.github.io/esgf-user-support/faq.html#how-to-preserve-the-directory-structure
* The script for CMIP5 model data can be automatically re-generated and downloaded using the following link https://esgf-data.dkrz.de/esg-search/wget?download_structure=model&project=CMIP5&experiment=historicalExt&variable=ta&ensemble=r2i1p1&time_frequency=mon.
* The script for observed (reference) data can be automatically re-generated and downloaded using the following link https://esgf-data.dkrz.de/esg-search/wget/?distrib=false&dataset_id=obs4MIPs.NASA-JPL.AIRS-1-0.mon.ta.gn.v20110608|aims3.llnl.gov.


## Code
|Source Code|Description|
|---|---|
|[src/](src/)|contains all source scripts.
|[src/app.py](src/app.py)|contains the main script used to build the dashboard.
|[src/pages/small_multiple.py](src/pages/small_multiple.py)|contains the script that builds the page with the small multiple technique presented using the [data/Case_Study_Gaussian_Processes/](data/Case_Study_Gaussian_Processes/) data.
|[src/pages/overview_detail.py](src/pages/overview_detail.py)|contains the script that builds the page with the overview+detail technique presented using the [data/Case_Study_Climate/](data/Case_Study_Climate/) and [data/Case_Study_Ecoli/](data/Case_Study_Ecoli/) data.


## Running
### Locally
We recommend downloading the repository and running the dashboard locally due to more responsive interactions. After installing the dependencies from the [requirements.txt](requirements.txt), the user should run the following commands (Linux):

```bash
cd Polar-Diagrams-Dashboard/src
python app.py
```

The user should then open the link shown in the terminal or open the browser and type the following address: `http://127.0.0.1:8050`.

### Online

The dashboard is also available online at: [https://polar-diagrams-dashboard.onrender.com/](https://polar-diagrams-dashboard.onrender.com/). The online version might not be as responsive which is why we recommend running the dashboard locally using the previously mentioned method.

## License

Licensed under the GNU General Public License, Version 3.0 ([LICENSE](LICENSE) or https://www.gnu.org/licenses/gpl-3.0.en.html)

## Contribution

Any contribution intentionally submitted for inclusion in the work by you, shall be licensed under the GNU GPLv3.
