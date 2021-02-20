# Know_Your_Options

study the basic conceots of trading options.

## Setup

## 1. Install Anaconda

#### Windows:
https://docs.anaconda.com/anaconda/install/windows/


#### Mac:
https://docs.anaconda.com/anaconda/install/mac-os/


#### Linux:
https://docs.anaconda.com/anaconda/install/linux/


## 2. Set Up the Virtual Environment via Terminal 

#### Activate environtment and link your environment with Jupyter:

        conda create -n Know_Your_Options python=3.6

        conda activate Portfolio_Selection

        pip install ipykernel
        
        python -m ipykernel install --user --name=Know_Your_Options


## 3. Install Packages

### Core Data Analytics

#### Matrix operations

        numpy
        
#### Scientific operations

        scipy
        
#### DataFrame operations

        pandas
        
#### Statistical models

        statsmodels
        
#### Data visualization       

        matplotlib

### Finance

#### Reading financial data from the web

        pandas_datareader
        
#### Web scraper for yahoo finance

        yfinance

#### Finance database for industry data

       FinanceDatabase
       
#### Volatility modelling
        
        arch

#### Core optimization

        cvxopt
 
#### Wrapper to nicely interface into cvxopt

        cvxpy
        
#### Facebook's timeseries forecasting tool        

        prophet

### Data Visualization

#### Colorful data visualization

        seaborn

#### Interactive data visualization

        bokeh

#### Create maps and geographical visualization

        geoplotlib
        
#### New framework for plotting graphics

        Altair
        
#### Similar to R's ggplot2 using grammer of graphics

        plotnine
       

### Machine & Deep Learning

#### Core machine learning package

        scikit-learn
        
#### The first publicly available gradient boosting package. Released by Tianqi Chen (University of Washington, Seattle)

        xgboost
        
#### Gradient Boosted Decision Trees package (Microsoft)

        lightgbm
        
#### Gradient Boosting Decision Trees package (Yandex)

        catboost
        
#### High-level neural networks API

        keras

#### Deep learning package from Google

        Tensorflow
        

### Natural language processing (NLP)

#### Loughran-McDonald sentiment word lists to perform sentiment analysis (csv_file)

        https://drive.google.com/file/d/12ECPJMxV2wSalXG8ykMmkpa1fq_ur0Rf/view

#### General NLP tasks

        nltk
        
#### Creating NLP prototypes quickly

        textblog
        
#### NLP applications for topic modelling, document similarity, etc.

        gensim

#### Web scraping

        scrapy

#### Production-level NLP library

        spacy

### Install Packages from GitHub:

- blitz

        git clone https://github.com/piEsposito/blitz-bayesian-deep-learning.git
        cd blitz-bayesian-deep-learning
        pip install .
        
- pyfolio

        git clone https://github.com/quantopian/pyfolio
        cd pyfolio
        pip install .

### Favourite JupyterLab extensions


#### nodejs

        conda install -c conda-forge nodejs


You can install plugins in Jupyter lab by clicking the jigsaw icon on the menu bar on the menu bar on the right of the editor.


#### Table of contents

        toc
        
#### Variable inspector in Jupyter Lab

        jupyterlab_variableInspector
        
#### Allows you to edit the notebook metadata

        jupyterlab_nbmetadata
        
#### Jump to definition of a variable or function in JupyterLab notebook and file editor

        jupyterlab_go_to_definition


#### Installing Jupyter notebook extensions
        
        conda install -c conda-forge jupyter_contrib_nbextensions