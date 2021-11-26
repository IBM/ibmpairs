#!/usr/bin/env python
import numpy
import pandas
from copy import copy, deepcopy

import rpy2.robjects as ro
from rpy2.robjects import r, pandas2ri, numpy2ri
from rpy2.robjects.conversion import localconverter
pandas2ri.activate()
numpy2ri.activate()
r.library("lme4")

class lmer(object):
    """
    Mixed effect regression
    Wrapper around lme4's lmer class to enable:
        - training
        - predicting
    """
    # Class wide constants/parameters

    def __init__(
        self,
        target                = None,
        fixed_effects         = [],
        re_features           = [],
        re_terms              = [],
    ):
        # Target
        self.target                   = target
        # Exhaustive list of fixed effects (used to prepare DataFrame)
        self.fixed_effects            = fixed_effects
        # Exhaustive list of random effects features including those used for intercept and/or slope as well as nested.
        self.re_features              = re_features
        # List of Random Effect Terms of the form (1|RE), (FE|RE), (1|RE1/RE2), or (FE|RE1/RE2)
        self.re_terms                 = re_terms
        # Training Dataset
        self.df_train                 = None
        # R DataFrame Names
        self.r_df_train_name          = None
        self.r_df_predict_name        = None
        # Fitted Model Name
        self.model_name               = None
        # Mixed Effects Formula
        self.formula                  = None
        # R strings
        self.r_train_string           = None
        self.r_predict_string         = None
        # Fitted Model parameters
        self.fe_coefficients          = None
        self.fe_params                = None
        self.re_params                = None
        # Predictions DataFrame
        self.df_preds                 = None
        
    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
    
    def import_clean_trainSet(self, df_train, verbose = False):
        """
        """
        self.df_train = df_train
        
        self.df_train = self.df_train[['year'] + self.fixed_effects + self.re_features + [self.target]]
        if verbose:
            print(self.df_train.tail())
   
    @staticmethod
    def pandas2R(r_df_name, df, verbose = False):
        """
        Handing over pandas to R
        :r_df_name:   Name of the DataFrame in R
        :df:          Pandas DataFrame
        """
        with localconverter(ro.default_converter + pandas2ri.converter):
            ro.globalenv[r_df_name] = ro.conversion.py2rpy(df)
    
    def prep_R_training(self,
                        prefix_df = 'r_df_train',
                        verbose = False):
        """
        Method for generating the string for lmer mixed effect model.
        Default is random intercept (no random slopes)

        :re_terms:              list of random effect terms
        :returns:               concatenated model string with the correct syntax.

        """
        # Compose the DataFrame name as used in R
        self.r_df_train_name = prefix_df
        
        # Handing over pandas to R
        self.pandas2R(self.r_df_train_name, self.df_train, verbose=False)

        # Compose the model name as used in R
        self.model_name = 'lm1'
        
        # Compose the model formula
        self.formula = 'cbind(' + self.target + ") ~ "
        first_term = True
        
        for i, f in enumerate(self.fixed_effects): 
            if first_term: 
                self.formula += f
                first_term = False
            else: 
                self.formula += " + " + f

        for i, r in enumerate(self.re_terms): 
            if first_term: 
                self.formula += r
                first_term = False
            else: 
                self.formula += " + " + r

        # Compose the model string
        self.r_train_string = self.model_name + ' <- lmer("' + self.formula + '",data=' + self.r_df_train_name + ')'
        if verbose:
            print(self.r_df_train_name)
            print(self.model_name)
            print(self.formula)
            print(self.r_train_string)

    @staticmethod
    def fe2df(model_name):
        """
        R Fixed effects parameters to Pandas DataFrame
        """
        fe_coefficients = pandas.DataFrame([r('fixef(' + model_name + ')')],
                                           index=['Estimate'],
                                           columns=r('names(fixef(' + model_name + '))')
                                          )
        fe_params = fe_coefficients.loc[['Estimate']]
        return fe_coefficients, fe_params

    @staticmethod
    def re2df(r_ranef):
        """
        R Random effect parameters to Pandas DataFrame
        r_ranef: r('ranef(lm1)')
        """
        re_params = {}
        for i, re_name in enumerate(r_ranef.names):
            with localconverter(ro.default_converter + pandas2ri.converter):
                re_params[re_name] = ro.conversion.rpy2py(r_ranef[i])
            re_params[re_name] = re_params[re_name].reset_index()
            re_params[re_name] = re_params[re_name].rename(columns={'index': re_name})
        return re_params

    def train_lmer(self, verbose=True):
        """
        Fit the model using R lmer function
        """
        if verbose:
            print(r(self.r_train_string))
        else:
            r(self.r_train_string)

        # Get the fixed-effect parameters
        self.fe_coefficients, self.fe_params = self.fe2df(self.model_name)

        # Get the random-effect parameters
        self.re_params = self.re2df(r('ranef(' + self.model_name + ')'))

        
    def predict_lmer(self, df_predict, prefix_df = 'r_df_predict'):
        """
        Predict using the lmer function
        :df_predict:  DataFrame with the data for the prediction
        """
        #self.df_predict = df_predict
        
        # Compose the DataFrame name as used in R
        self.r_df_predict_name = prefix_df

        # Handing over pandas to R
        self.pandas2R(self.r_df_predict_name, df_predict, verbose=False)

        # Compose the r_string
        self.r_predict_string = 'predict(' + self.model_name + ', newdata=' +\
                                self.r_df_predict_name + ', allow.new.levels=TRUE)'

        # Run the prediction
        self.df_preds = pandas.DataFrame(r(self.r_predict_string))

        # Convert to probabilities and either-or predictions
        self.df_preds = self.df_preds.rename(columns={0:'preds'})
        
        # Concatenate prediction DataFrame
        #self.df_preds = pandas.concat([df_predict, self.df_preds], axis=1)
