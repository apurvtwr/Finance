from django.db import models
import pandas as pd
from datetime import datetime
import json
from yahoofinancials import YahooFinancials

# Create your models here.

class Company(models.Model) :
    ticker = models.TextField(unique=True)
    name = models.TextField(blank=True, null=True)
    
    def refresh(self) :
        yahoo_financials = YahooFinancials([self.ticker])
        data = yahoo_financials.get_financial_stmts('annual', ['income', 'cash', 'balance'])
        income_stm = json.dumps(data['incomeStatementHistory'][self.ticker])
        balance_sheet = json.dumps(data['balanceSheetHistory'][self.ticker])
        cashflow_stm = json.dumps(data['cashflowStatementHistory'][self.ticker])
        
        bs_data = BalanceSheet.objects.filter(company=self).order_by('-created_at')
        if len(bs_data) == 0 or bs_data[0].data != balance_sheet:
            bs = BalanceSheet(company=self, data=balance_sheet)
            bs.save()
        
        is_data = IncomeStatement.objects.filter(company=self).order_by('-created_at')
        if len(is_data) == 0 or is_data[0].data != income_stm:
            iss = IncomeStatement(company=self, data=income_stm)
            iss.save()
        
        cfs_data = CashFlowStatement.objects.filter(company=self).order_by('-created_at')
        if len(cfs_data) == 0 or cfs_data[0].data != cashflow_stm:
            cfs = CashFlowStatement(company=self, data=cashflow_stm)
            cfs.save()
        

class BalanceSheet(models.Model) :
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class IncomeStatement(models.Model) :
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CashFlowStatement(models.Model) :
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)