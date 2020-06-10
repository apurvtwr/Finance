from django.db import models
import pandas as pd
from datetime import datetime
import json

# Create your models here.

class Company(models.Model) :
    ticker = models.TextField(unique=True)
    name = models.TextField(blank=True, null=True)

class BalanceSheet(models.Model) :
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    _multiplier = 1e3
    
    @property
    def df(self) :
        return pd.read_json(self.data)
    
    @property
    def dates(self) :
        dates = []
        for date in self.df.columns[1:] :
            dates.append(datetime.strptime(date, '%m/%d/%Y'))
        
        return dates
    
    def _data_selector(self, column_name, date=None) :
        if not date :
            date = datetime.now()
        
        index = 0
        for index in range(len(self.dates)) :
            _date = self.dates[index]
            if date > _date :
                break
        
        return self.df[self.df['Breakdown'] == column_name].to_numpy()[0, index + 1] * self._multiplier
    
    def total_assets(self, date=None) :
        column_name = 'Total Assets'
        return self._data_selector(column_name, date)
    
    def net_tangible_assets(self, date=None) :
        column_name = 'Net Tangible Assets'
        return self._data_selector(column_name, date)
    
    def enterprise_value(self, date=None) :
        column_name = 'Total Capitalization'
        return self._data_selector(column_name, date)
    
    def net_debt(self, date=None) :
        column_name = 'Net Debt'
        return self._data_selector(column_name, date)
    
    def total_debt(self, date=None) :
        column_name = 'Total Debt'
        return self._data_selector(column_name, date)

class QuoteTable(models.Model) :
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def _quote(self) :
        return json.loads(self.data)
    
    def market_cap(x) :
        m_cap = self._quote["Market Cap"]
        if m_cap.endswith("T") :
            return float(m_cap[:-1]) * 1e12
        if m_cap.endswith("B") :
            return float(m_cap[:-1]) * 1e9
        if m_cap.endswith("M") :
            return float(m_cap[:-1]) * 1e6
        return float(m_cap)
