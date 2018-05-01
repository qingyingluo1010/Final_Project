from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import InputData as Data
import scr.MarkovClasses as MarkovCls
import scr.RandomVariantGenerators as Random


class HealthStats(Enum):
    """ health states of patients with HIV """
    ProgressFree = 0
    Progress = 1
    Death = 2


class Therapies(Enum):
    """ mono vs. combination therapy """
    NONE = 0
    COMBO = 1


class ParametersFixed():
    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        if self._therapy == Therapies.MONO:
            self._delta_t = Data.DELTA_T_G
        else:
            self._delta_t = Data.DELTA_T_GC

        # calculate the adjusted discount rate
        if self._therapy == Therapies.MONO:
            self._adjDiscountRate = Data.DISCOUNT * Data.DELTA_T_G
        else:
            self._adjDiscountRate = Data.DISCOUNT * Data.DELTA_T_GC

        # initial health state
        self._initialHealthState = HealthStats.ProgressFree

        # annual treatment cost
        if self._therapy == Therapies.MONO:
            self._annualTreatmentCost = 0
        else:
            self._annualTreatmentCost = Data.GC_COST

        # transition rate matrix of the selected therapy
        self._rate_matrix = []
        self._prob_matrix = []
        # treatment relative risk
        self._treatmentRR = 0

        # calculate transition probabilities depending of which therapy options is in use
        if therapy == Therapies.MONO:
            self._rate_matrix = Data.TRANS_MATRIX
            # convert rate to probability
            self._prob_matrix[:], p = MarkovCls.continuous_to_discrete(self._rate_matrix, Data.DELTA_T_G)
           # print('Upper bound on the probability of two transitions within delta_t:', p)
        else:
            self._rate_matrix = Data.TRANS_MATRIX_GC
            self._prob_matrix[:], p = MarkovCls.continuous_to_discrete(self._rate_matrix, Data.DELTA_T_GC)
           # print('Upper bound on the probability of two transitions within delta_t:', p)

        # annual state costs and utilities
        self._annualStateCosts = Data.MONTHLY_STATE_COST
        self._annualStateUtilities = Data.MONTHLY_STATE_Utility

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_annual_state_cost(self,state):
        if state == HealthStats.DEATH:
            return 0
        else:
            return  self._annualStateCosts[state.value]

    def get_annual_state_utility(self,state):
        if state == HealthStats.DEATH:
            return 0
        else:
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost