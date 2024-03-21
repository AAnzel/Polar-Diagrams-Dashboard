# Polar-Diagrams-Dashboard
## Manuscript

This library is created for the following paper:

***"A Multi-Technique Strategy for Enhancing Polar Diagrams"*** by Aleksandar Anžel, Zewen Yang, and Georges Hattab

Please cite the paper as:
```latex

```

---
Abstract:

> __Objective__: 
Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum 

> __Methods__:
Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum 

>__Results__:
Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum 

>__Conclusion__:
Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum 



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
|[data/](data/)|contains all datasets used in the dashboard.
|[data/Case_Study_Climate/](data/Case_Study_Climate/)|contains the Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum
|[data/Case_Study_Ecoli/](data/Case_Study_Ecoli/)|contains the Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum
|[data/Case_Study_Gaussian_Processes/](data/Case_Study_Gaussian_Processes/)|contains the Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum


**[1]** The script used for downloading the [data/Case_Study_Climate/](data/Case_Study_Climate/) was generated using the tutorial found here Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum
Script can be automatically generated and downloaded again from here Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum

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

### Contribution

Any contribution intentionally submitted for inclusion in the work by you, shall be licensed under the GNU GPLv3.
