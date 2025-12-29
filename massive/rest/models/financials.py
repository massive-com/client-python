from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from ...modelclass import modelclass


@modelclass
@dataclass
class DataPoint:
    """Represents a single numeric or textual data point in the financials."""

    label: Optional[str] = None
    order: Optional[int] = None
    unit: Optional[str] = None
    value: Optional[float] = None
    derived_from: Optional[List[str]] = None
    formula: Optional[str] = None
    source: Optional[Dict[str, str]] = None
    xpath: Optional[str] = None

    @staticmethod
    def from_dict(d: Optional[Dict[str, Any]]) -> "DataPoint":
        if not d:
            return DataPoint()
        return DataPoint(
            label=d.get("label"),
            order=d.get("order"),
            unit=d.get("unit"),
            value=d.get("value"),
            derived_from=d.get("derived_from"),
            formula=d.get("formula"),
            source=d.get("source"),
            xpath=d.get("xpath"),
        )


@dataclass
@modelclass
class BalanceSheet:
    assets: Optional[DataPoint] = None
    current_assets: Optional[DataPoint] = None
    cash: Optional[DataPoint] = None
    accounts_receivable: Optional[DataPoint] = None
    inventory: Optional[DataPoint] = None
    prepaid_expenses: Optional[DataPoint] = None
    other_current_assets: Optional[DataPoint] = None
    noncurrent_assets: Optional[DataPoint] = None
    long_term_investments: Optional[DataPoint] = None
    fixed_assets: Optional[DataPoint] = None
    intangible_assets: Optional[DataPoint] = None
    noncurrent_prepaid_expense: Optional[DataPoint] = None
    other_noncurrent_assets: Optional[DataPoint] = None
    liabilities: Optional[DataPoint] = None
    current_liabilities: Optional[DataPoint] = None
    accounts_payable: Optional[DataPoint] = None
    interest_payable: Optional[DataPoint] = None
    wages: Optional[DataPoint] = None
    other_current_liabilities: Optional[DataPoint] = None
    noncurrent_liabilities: Optional[DataPoint] = None
    long_term_debt: Optional[DataPoint] = None
    other_noncurrent_liabilities: Optional[DataPoint] = None
    commitments_and_contingencies: Optional[DataPoint] = None
    redeemable_noncontrolling_interest: Optional[DataPoint] = None
    redeemable_noncontrolling_interest_common: Optional[DataPoint] = None
    redeemable_noncontrolling_interest_other: Optional[DataPoint] = None
    redeemable_noncontrolling_interest_preferred: Optional[DataPoint] = None
    equity: Optional[DataPoint] = None
    equity_attributable_to_noncontrolling_interest: Optional[DataPoint] = None
    equity_attributable_to_parent: Optional[DataPoint] = None
    temporary_equity: Optional[DataPoint] = None
    temporary_equity_attributable_to_parent: Optional[DataPoint] = None
    liabilities_and_equity: Optional[DataPoint] = None

    @staticmethod
    def from_dict(d: Optional[Dict[str, Any]]) -> "BalanceSheet":
        if not d:
            return BalanceSheet()
        return BalanceSheet(
            assets=DataPoint.from_dict(d.get("assets")),
            current_assets=DataPoint.from_dict(d.get("current_assets")),
            cash=DataPoint.from_dict(d.get("cash")),
            accounts_receivable=DataPoint.from_dict(d.get("accounts_receivable")),
            inventory=DataPoint.from_dict(d.get("inventory")),
            prepaid_expenses=DataPoint.from_dict(d.get("prepaid_expenses")),
            other_current_assets=DataPoint.from_dict(d.get("other_current_assets")),
            noncurrent_assets=DataPoint.from_dict(d.get("noncurrent_assets")),
            long_term_investments=DataPoint.from_dict(d.get("long_term_investments")),
            fixed_assets=DataPoint.from_dict(d.get("fixed_assets")),
            intangible_assets=DataPoint.from_dict(d.get("intangible_assets")),
            noncurrent_prepaid_expense=DataPoint.from_dict(
                d.get("noncurrent_prepaid_expense")
            ),
            other_noncurrent_assets=DataPoint.from_dict(
                d.get("other_noncurrent_assets")
            ),
            liabilities=DataPoint.from_dict(d.get("liabilities")),
            current_liabilities=DataPoint.from_dict(d.get("current_liabilities")),
            accounts_payable=DataPoint.from_dict(d.get("accounts_payable")),
            interest_payable=DataPoint.from_dict(d.get("interest_payable")),
            wages=DataPoint.from_dict(d.get("wages")),
            other_current_liabilities=DataPoint.from_dict(
                d.get("other_current_liabilities")
            ),
            noncurrent_liabilities=DataPoint.from_dict(d.get("noncurrent_liabilities")),
            long_term_debt=DataPoint.from_dict(d.get("long_term_debt")),
            other_noncurrent_liabilities=DataPoint.from_dict(
                d.get("other_noncurrent_liabilities")
            ),
            commitments_and_contingencies=DataPoint.from_dict(
                d.get("commitments_and_contingencies")
            ),
            redeemable_noncontrolling_interest=DataPoint.from_dict(
                d.get("redeemable_noncontrolling_interest")
            ),
            redeemable_noncontrolling_interest_common=DataPoint.from_dict(
                d.get("redeemable_noncontrolling_interest_common")
            ),
            redeemable_noncontrolling_interest_other=DataPoint.from_dict(
                d.get("redeemable_noncontrolling_interest_other")
            ),
            redeemable_noncontrolling_interest_preferred=DataPoint.from_dict(
                d.get("redeemable_noncontrolling_interest_preferred")
            ),
            equity=DataPoint.from_dict(d.get("equity")),
            equity_attributable_to_noncontrolling_interest=DataPoint.from_dict(
                d.get("equity_attributable_to_noncontrolling_interest")
            ),
            equity_attributable_to_parent=DataPoint.from_dict(
                d.get("equity_attributable_to_parent")
            ),
            temporary_equity=DataPoint.from_dict(d.get("temporary_equity")),
            temporary_equity_attributable_to_parent=DataPoint.from_dict(
                d.get("temporary_equity_attributable_to_parent")
            ),
            liabilities_and_equity=DataPoint.from_dict(d.get("liabilities_and_equity")),
        )


@dataclass
@modelclass
class CashFlowStatement:
    net_cash_flow_from_operating_activities: Optional[DataPoint] = None
    net_cash_flow_from_operating_activities_continuing: Optional[DataPoint] = None
    net_cash_flow_from_operating_activities_discontinued: Optional[DataPoint] = None
    net_cash_flow_from_investing_activities: Optional[DataPoint] = None
    net_cash_flow_from_investing_activities_continuing: Optional[DataPoint] = None
    net_cash_flow_from_investing_activities_discontinued: Optional[DataPoint] = None
    net_cash_flow_from_financing_activities: Optional[DataPoint] = None
    net_cash_flow_from_financing_activities_continuing: Optional[DataPoint] = None
    net_cash_flow_from_financing_activities_discontinued: Optional[DataPoint] = None
    exchange_gains_losses: Optional[DataPoint] = None
    net_cash_flow: Optional[DataPoint] = None
    net_cash_flow_continuing: Optional[DataPoint] = None
    net_cash_flow_discontinued: Optional[DataPoint] = None

    @staticmethod
    def from_dict(d: Optional[Dict[str, Any]]) -> "CashFlowStatement":
        if not d:
            return CashFlowStatement()
        return CashFlowStatement(
            net_cash_flow_from_operating_activities=DataPoint.from_dict(
                d.get("net_cash_flow_from_operating_activities")
            ),
            net_cash_flow_from_operating_activities_continuing=DataPoint.from_dict(
                d.get("net_cash_flow_from_operating_activities_continuing")
            ),
            net_cash_flow_from_operating_activities_discontinued=DataPoint.from_dict(
                d.get("net_cash_flow_from_operating_activities_discontinued")
            ),
            net_cash_flow_from_investing_activities=DataPoint.from_dict(
                d.get("net_cash_flow_from_investing_activities")
            ),
            net_cash_flow_from_investing_activities_continuing=DataPoint.from_dict(
                d.get("net_cash_flow_from_investing_activities_continuing")
            ),
            net_cash_flow_from_investing_activities_discontinued=DataPoint.from_dict(
                d.get("net_cash_flow_from_investing_activities_discontinued")
            ),
            net_cash_flow_from_financing_activities=DataPoint.from_dict(
                d.get("net_cash_flow_from_financing_activities")
            ),
            net_cash_flow_from_financing_activities_continuing=DataPoint.from_dict(
                d.get("net_cash_flow_from_financing_activities_continuing")
            ),
            net_cash_flow_from_financing_activities_discontinued=DataPoint.from_dict(
                d.get("net_cash_flow_from_financing_activities_discontinued")
            ),
            exchange_gains_losses=DataPoint.from_dict(d.get("exchange_gains_losses")),
            net_cash_flow=DataPoint.from_dict(d.get("net_cash_flow")),
            net_cash_flow_continuing=DataPoint.from_dict(
                d.get("net_cash_flow_continuing")
            ),
            net_cash_flow_discontinued=DataPoint.from_dict(
                d.get("net_cash_flow_discontinued")
            ),
        )


@dataclass
@modelclass
class ComprehensiveIncome:
    comprehensive_income_loss: Optional[DataPoint] = None
    comprehensive_income_loss_attributable_to_noncontrolling_interest: Optional[
        DataPoint
    ] = None
    comprehensive_income_loss_attributable_to_parent: Optional[DataPoint] = None
    other_comprehensive_income_loss: Optional[DataPoint] = None
    other_comprehensive_income_loss_attributable_to_noncontrolling_interest: Optional[
        DataPoint
    ] = None
    other_comprehensive_income_loss_attributable_to_parent: Optional[DataPoint] = None

    @staticmethod
    def from_dict(d: Optional[Dict[str, Any]]) -> "ComprehensiveIncome":
        if not d:
            return ComprehensiveIncome()
        return ComprehensiveIncome(
            comprehensive_income_loss=DataPoint.from_dict(
                d.get("comprehensive_income_loss")
            ),
            comprehensive_income_loss_attributable_to_noncontrolling_interest=DataPoint.from_dict(
                d.get(
                    "comprehensive_income_loss_attributable_to_noncontrolling_interest"
                )
            ),
            comprehensive_income_loss_attributable_to_parent=DataPoint.from_dict(
                d.get("comprehensive_income_loss_attributable_to_parent")
            ),
            other_comprehensive_income_loss=DataPoint.from_dict(
                d.get("other_comprehensive_income_loss")
            ),
            other_comprehensive_income_loss_attributable_to_noncontrolling_interest=DataPoint.from_dict(
                d.get(
                    "other_comprehensive_income_loss_attributable_to_noncontrolling_interest"
                )
            ),
            other_comprehensive_income_loss_attributable_to_parent=DataPoint.from_dict(
                d.get("other_comprehensive_income_loss_attributable_to_parent")
            ),
        )


@dataclass
@modelclass
class IncomeStatement:
    revenues: Optional[DataPoint] = None
    benefits_costs_expenses: Optional[DataPoint] = None
    cost_of_revenue: Optional[DataPoint] = None
    cost_of_revenue_goods: Optional[DataPoint] = None
    cost_of_revenue_services: Optional[DataPoint] = None
    costs_and_expenses: Optional[DataPoint] = None
    gross_profit: Optional[DataPoint] = None
    gain_loss_on_sale_properties_net_tax: Optional[DataPoint] = None
    nonoperating_income_loss: Optional[DataPoint] = None
    operating_expenses: Optional[DataPoint] = None
    selling_general_and_administrative_expenses: Optional[DataPoint] = None
    depreciation_and_amortization: Optional[DataPoint] = None
    research_and_development: Optional[DataPoint] = None
    other_operating_expenses: Optional[DataPoint] = None
    operating_income_loss: Optional[DataPoint] = None
    other_operating_income_expenses: Optional[DataPoint] = None
    income_loss_before_equity_method_investments: Optional[DataPoint] = None
    income_loss_from_continuing_operations_after_tax: Optional[DataPoint] = None
    income_loss_from_continuing_operations_before_tax: Optional[DataPoint] = None
    income_loss_from_discontinued_operations_net_of_tax: Optional[DataPoint] = None
    income_loss_from_discontinued_operations_net_of_tax_adjustment_to_prior_year_gain_loss_on_disposal: Optional[
        DataPoint
    ] = None
    income_loss_from_discontinued_operations_net_of_tax_during_phase_out: Optional[
        DataPoint
    ] = None
    income_loss_from_discontinued_operations_net_of_tax_gain_loss_on_disposal: Optional[
        DataPoint
    ] = None
    income_loss_from_discontinued_operations_net_of_tax_provision_for_gain_loss_on_disposal: Optional[
        DataPoint
    ] = None
    income_loss_from_equity_method_investments: Optional[DataPoint] = None
    income_tax_expense_benefit: Optional[DataPoint] = None
    income_tax_expense_benefit_current: Optional[DataPoint] = None
    income_tax_expense_benefit_deferred: Optional[DataPoint] = None
    interest_and_debt_expense: Optional[DataPoint] = None
    interest_and_dividend_income_operating: Optional[DataPoint] = None
    interest_expense_operating: Optional[DataPoint] = None
    interest_income_expense_after_provision_for_losses: Optional[DataPoint] = None
    interest_income_expense_operating_net: Optional[DataPoint] = None
    noninterest_expense: Optional[DataPoint] = None
    noninterest_income: Optional[DataPoint] = None
    provision_for_loan_lease_and_other_losses: Optional[DataPoint] = None
    net_income_loss: Optional[DataPoint] = None
    net_income_loss_attributable_to_noncontrolling_interest: Optional[DataPoint] = None
    net_income_loss_attributable_to_nonredeemable_noncontrolling_interest: Optional[
        DataPoint
    ] = None
    net_income_loss_attributable_to_parent: Optional[DataPoint] = None
    net_income_loss_attributable_to_redeemable_noncontrolling_interest: Optional[
        DataPoint
    ] = None
    net_income_loss_available_to_common_stockholders_basic: Optional[DataPoint] = None
    participating_securities_distributed_and_undistributed_earnings_loss_basic: (
        Optional[DataPoint]
    ) = (None)
    undistributed_earnings_loss_allocated_to_participating_securities_basic: Optional[
        DataPoint
    ] = None
    preferred_stock_dividends_and_other_adjustments: Optional[DataPoint] = None
    basic_earnings_per_share: Optional[DataPoint] = None
    diluted_earnings_per_share: Optional[DataPoint] = None
    basic_average_shares: Optional[DataPoint] = None
    diluted_average_shares: Optional[DataPoint] = None
    common_stock_dividends: Optional[DataPoint] = None

    @staticmethod
    def from_dict(d: Optional[Dict[str, Any]]) -> "IncomeStatement":
        if not d:
            return IncomeStatement()
        return IncomeStatement(
            revenues=DataPoint.from_dict(d.get("revenues")),
            benefits_costs_expenses=DataPoint.from_dict(
                d.get("benefits_costs_expenses")
            ),
            cost_of_revenue=DataPoint.from_dict(d.get("cost_of_revenue")),
            cost_of_revenue_goods=DataPoint.from_dict(d.get("cost_of_revenue_goods")),
            cost_of_revenue_services=DataPoint.from_dict(
                d.get("cost_of_revenue_services")
            ),
            costs_and_expenses=DataPoint.from_dict(d.get("costs_and_expenses")),
            gross_profit=DataPoint.from_dict(d.get("gross_profit")),
            gain_loss_on_sale_properties_net_tax=DataPoint.from_dict(
                d.get("gain_loss_on_sale_properties_net_tax")
            ),
            nonoperating_income_loss=DataPoint.from_dict(
                d.get("nonoperating_income_loss")
            ),
            operating_expenses=DataPoint.from_dict(d.get("operating_expenses")),
            selling_general_and_administrative_expenses=DataPoint.from_dict(
                d.get("selling_general_and_administrative_expenses")
            ),
            depreciation_and_amortization=DataPoint.from_dict(
                d.get("depreciation_and_amortization")
            ),
            research_and_development=DataPoint.from_dict(
                d.get("research_and_development")
            ),
            other_operating_expenses=DataPoint.from_dict(
                d.get("other_operating_expenses")
            ),
            operating_income_loss=DataPoint.from_dict(d.get("operating_income_loss")),
            other_operating_income_expenses=DataPoint.from_dict(
                d.get("other_operating_income_expenses")
            ),
            income_loss_before_equity_method_investments=DataPoint.from_dict(
                d.get("income_loss_before_equity_method_investments")
            ),
            income_loss_from_continuing_operations_after_tax=DataPoint.from_dict(
                d.get("income_loss_from_continuing_operations_after_tax")
            ),
            income_loss_from_continuing_operations_before_tax=DataPoint.from_dict(
                d.get("income_loss_from_continuing_operations_before_tax")
            ),
            income_loss_from_discontinued_operations_net_of_tax=DataPoint.from_dict(
                d.get("income_loss_from_discontinued_operations_net_of_tax")
            ),
            income_loss_from_discontinued_operations_net_of_tax_adjustment_to_prior_year_gain_loss_on_disposal=DataPoint.from_dict(
                d.get(
                    "income_loss_from_discontinued_operations_net_of_tax_adjustment_to_prior_year_gain_loss_on_disposal"
                )
            ),
            income_loss_from_discontinued_operations_net_of_tax_during_phase_out=DataPoint.from_dict(
                d.get(
                    "income_loss_from_discontinued_operations_net_of_tax_during_phase_out"
                )
            ),
            income_loss_from_discontinued_operations_net_of_tax_gain_loss_on_disposal=DataPoint.from_dict(
                d.get(
                    "income_loss_from_discontinued_operations_net_of_tax_gain_loss_on_disposal"
                )
            ),
            income_loss_from_discontinued_operations_net_of_tax_provision_for_gain_loss_on_disposal=DataPoint.from_dict(
                d.get(
                    "income_loss_from_discontinued_operations_net_of_tax_provision_for_gain_loss_on_disposal"
                )
            ),
            income_loss_from_equity_method_investments=DataPoint.from_dict(
                d.get("income_loss_from_equity_method_investments")
            ),
            income_tax_expense_benefit=DataPoint.from_dict(
                d.get("income_tax_expense_benefit")
            ),
            income_tax_expense_benefit_current=DataPoint.from_dict(
                d.get("income_tax_expense_benefit_current")
            ),
            income_tax_expense_benefit_deferred=DataPoint.from_dict(
                d.get("income_tax_expense_benefit_deferred")
            ),
            interest_and_debt_expense=DataPoint.from_dict(
                d.get("interest_and_debt_expense")
            ),
            interest_and_dividend_income_operating=DataPoint.from_dict(
                d.get("interest_and_dividend_income_operating")
            ),
            interest_expense_operating=DataPoint.from_dict(
                d.get("interest_expense_operating")
            ),
            interest_income_expense_after_provision_for_losses=DataPoint.from_dict(
                d.get("interest_income_expense_after_provision_for_losses")
            ),
            interest_income_expense_operating_net=DataPoint.from_dict(
                d.get("interest_income_expense_operating_net")
            ),
            noninterest_expense=DataPoint.from_dict(d.get("noninterest_expense")),
            noninterest_income=DataPoint.from_dict(d.get("noninterest_income")),
            provision_for_loan_lease_and_other_losses=DataPoint.from_dict(
                d.get("provision_for_loan_lease_and_other_losses")
            ),
            net_income_loss=DataPoint.from_dict(d.get("net_income_loss")),
            net_income_loss_attributable_to_noncontrolling_interest=DataPoint.from_dict(
                d.get("net_income_loss_attributable_to_noncontrolling_interest")
            ),
            net_income_loss_attributable_to_nonredeemable_noncontrolling_interest=DataPoint.from_dict(
                d.get(
                    "net_income_loss_attributable_to_nonredeemable_noncontrolling_interest"
                )
            ),
            net_income_loss_attributable_to_parent=DataPoint.from_dict(
                d.get("net_income_loss_attributable_to_parent")
            ),
            net_income_loss_attributable_to_redeemable_noncontrolling_interest=DataPoint.from_dict(
                d.get(
                    "net_income_loss_attributable_to_redeemable_noncontrolling_interest"
                )
            ),
            net_income_loss_available_to_common_stockholders_basic=DataPoint.from_dict(
                d.get("net_income_loss_available_to_common_stockholders_basic")
            ),
            participating_securities_distributed_and_undistributed_earnings_loss_basic=DataPoint.from_dict(
                d.get(
                    "participating_securities_distributed_and_undistributed_earnings_loss_basic"
                )
            ),
            undistributed_earnings_loss_allocated_to_participating_securities_basic=DataPoint.from_dict(
                d.get(
                    "undistributed_earnings_loss_allocated_to_participating_securities_basic"
                )
            ),
            preferred_stock_dividends_and_other_adjustments=DataPoint.from_dict(
                d.get("preferred_stock_dividends_and_other_adjustments")
            ),
            basic_earnings_per_share=DataPoint.from_dict(
                d.get("basic_earnings_per_share")
            ),
            diluted_earnings_per_share=DataPoint.from_dict(
                d.get("diluted_earnings_per_share")
            ),
            basic_average_shares=DataPoint.from_dict(d.get("basic_average_shares")),
            diluted_average_shares=DataPoint.from_dict(d.get("diluted_average_shares")),
            common_stock_dividends=DataPoint.from_dict(d.get("common_stock_dividends")),
        )


@dataclass
@modelclass
class Financials:
    """
    Contains data for:
      - balance_sheet (BalanceSheet)
      - cash_flow_statement (CashFlowStatement)
      - comprehensive_income (ComprehensiveIncome)
      - income_statement (IncomeStatement)
    """

    balance_sheet: Optional[BalanceSheet] = None
    cash_flow_statement: Optional[CashFlowStatement] = None
    comprehensive_income: Optional[ComprehensiveIncome] = None
    income_statement: Optional[IncomeStatement] = None

    @staticmethod
    def from_dict(d: Optional[Dict[str, Any]]) -> "Financials":
        if not d:
            return Financials()
        return Financials(
            balance_sheet=BalanceSheet.from_dict(d.get("balance_sheet")),
            cash_flow_statement=CashFlowStatement.from_dict(
                d.get("cash_flow_statement")
            ),
            comprehensive_income=ComprehensiveIncome.from_dict(
                d.get("comprehensive_income")
            ),
            income_statement=IncomeStatement.from_dict(d.get("income_statement")),
        )


@dataclass
@modelclass
class StockFinancial:
    """
    StockFinancial contains historical financial data for a stock ticker.
    The 'financials' attribute references an instance of Financials
    which has typed sub-statements.
    """

    cik: Optional[str] = None
    company_name: Optional[str] = None
    end_date: Optional[str] = None
    filing_date: Optional[str] = None
    financials: Optional[Financials] = None
    fiscal_period: Optional[str] = None
    fiscal_year: Optional[str] = None
    source_filing_file_url: Optional[str] = None
    source_filing_url: Optional[str] = None
    start_date: Optional[str] = None

    @staticmethod
    def from_dict(d: Optional[Dict[str, Any]]) -> "StockFinancial":
        if not d:
            return StockFinancial()
        return StockFinancial(
            cik=d.get("cik"),
            company_name=d.get("company_name"),
            end_date=d.get("end_date"),
            filing_date=d.get("filing_date"),
            financials=Financials.from_dict(d.get("financials", {})),
            fiscal_period=d.get("fiscal_period"),
            fiscal_year=d.get("fiscal_year"),
            source_filing_file_url=d.get("source_filing_file_url"),
            source_filing_url=d.get("source_filing_url"),
            start_date=d.get("start_date"),
        )


@modelclass
class FinancialBalanceSheet:
    accounts_payable: Optional[float] = None
    accrued_and_other_current_liabilities: Optional[float] = None
    accumulated_other_comprehensive_income: Optional[float] = None
    additional_paid_in_capital: Optional[float] = None
    cash_and_equivalents: Optional[float] = None
    cik: Optional[str] = None
    commitments_and_contingencies: Optional[float] = None
    common_stock: Optional[float] = None
    debt_current: Optional[float] = None
    deferred_revenue_current: Optional[float] = None
    filing_date: Optional[str] = None
    fiscal_quarter: Optional[float] = None
    fiscal_year: Optional[float] = None
    goodwill: Optional[float] = None
    intangible_assets_net: Optional[float] = None
    inventories: Optional[float] = None
    long_term_debt_and_capital_lease_obligations: Optional[float] = None
    noncontrolling_interest: Optional[float] = None
    other_assets: Optional[float] = None
    other_current_assets: Optional[float] = None
    other_equity: Optional[float] = None
    other_noncurrent_liabilities: Optional[float] = None
    period_end: Optional[str] = None
    preferred_stock: Optional[float] = None
    property_plant_equipment_net: Optional[float] = None
    receivables: Optional[float] = None
    retained_earnings_deficit: Optional[float] = None
    short_term_investments: Optional[float] = None
    tickers: Optional[List[str]] = None
    timeframe: Optional[str] = None
    total_assets: Optional[float] = None
    total_current_assets: Optional[float] = None
    total_current_liabilities: Optional[float] = None
    total_equity: Optional[float] = None
    total_equity_attributable_to_parent: Optional[float] = None
    total_liabilities: Optional[float] = None
    total_liabilities_and_equity: Optional[float] = None
    treasury_stock: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return FinancialBalanceSheet(
            accounts_payable=d.get("accounts_payable"),
            accrued_and_other_current_liabilities=d.get(
                "accrued_and_other_current_liabilities"
            ),
            accumulated_other_comprehensive_income=d.get(
                "accumulated_other_comprehensive_income"
            ),
            additional_paid_in_capital=d.get("additional_paid_in_capital"),
            cash_and_equivalents=d.get("cash_and_equivalents"),
            cik=d.get("cik"),
            commitments_and_contingencies=d.get("commitments_and_contingencies"),
            common_stock=d.get("common_stock"),
            debt_current=d.get("debt_current"),
            deferred_revenue_current=d.get("deferred_revenue_current"),
            filing_date=d.get("filing_date"),
            fiscal_quarter=d.get("fiscal_quarter"),
            fiscal_year=d.get("fiscal_year"),
            goodwill=d.get("goodwill"),
            intangible_assets_net=d.get("intangible_assets_net"),
            inventories=d.get("inventories"),
            long_term_debt_and_capital_lease_obligations=d.get(
                "long_term_debt_and_capital_lease_obligations"
            ),
            noncontrolling_interest=d.get("noncontrolling_interest"),
            other_assets=d.get("other_assets"),
            other_current_assets=d.get("other_current_assets"),
            other_equity=d.get("other_equity"),
            other_noncurrent_liabilities=d.get("other_noncurrent_liabilities"),
            period_end=d.get("period_end"),
            preferred_stock=d.get("preferred_stock"),
            property_plant_equipment_net=d.get("property_plant_equipment_net"),
            receivables=d.get("receivables"),
            retained_earnings_deficit=d.get("retained_earnings_deficit"),
            short_term_investments=d.get("short_term_investments"),
            tickers=d.get("tickers"),
            timeframe=d.get("timeframe"),
            total_assets=d.get("total_assets"),
            total_current_assets=d.get("total_current_assets"),
            total_current_liabilities=d.get("total_current_liabilities"),
            total_equity=d.get("total_equity"),
            total_equity_attributable_to_parent=d.get(
                "total_equity_attributable_to_parent"
            ),
            total_liabilities=d.get("total_liabilities"),
            total_liabilities_and_equity=d.get("total_liabilities_and_equity"),
            treasury_stock=d.get("treasury_stock"),
        )


@modelclass
class FinancialCashFlowStatement:
    cash_from_operating_activities_continuing_operations: Optional[float] = None
    change_in_cash_and_equivalents: Optional[float] = None
    change_in_other_operating_assets_and_liabilities_net: Optional[float] = None
    cik: Optional[str] = None
    depreciation_depletion_and_amortization: Optional[float] = None
    dividends: Optional[float] = None
    effect_of_currency_exchange_rate: Optional[float] = None
    filing_date: Optional[str] = None
    fiscal_quarter: Optional[float] = None
    fiscal_year: Optional[float] = None
    income_loss_from_discontinued_operations: Optional[float] = None
    long_term_debt_issuances_repayments: Optional[float] = None
    net_cash_from_financing_activities: Optional[float] = None
    net_cash_from_financing_activities_continuing_operations: Optional[float] = None
    net_cash_from_financing_activities_discontinued_operations: Optional[float] = None
    net_cash_from_investing_activities: Optional[float] = None
    net_cash_from_investing_activities_continuing_operations: Optional[float] = None
    net_cash_from_investing_activities_discontinued_operations: Optional[float] = None
    net_cash_from_operating_activities: Optional[float] = None
    net_cash_from_operating_activities_discontinued_operations: Optional[float] = None
    net_income: Optional[float] = None
    noncontrolling_interests: Optional[float] = None
    other_cash_adjustments: Optional[float] = None
    other_financing_activities: Optional[float] = None
    other_investing_activities: Optional[float] = None
    other_operating_activities: Optional[float] = None
    period_end: Optional[str] = None
    purchase_of_property_plant_and_equipment: Optional[float] = None
    sale_of_property_plant_and_equipment: Optional[float] = None
    short_term_debt_issuances_repayments: Optional[float] = None
    tickers: Optional[List[str]] = None
    timeframe: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return FinancialCashFlowStatement(
            cash_from_operating_activities_continuing_operations=d.get(
                "cash_from_operating_activities_continuing_operations"
            ),
            change_in_cash_and_equivalents=d.get("change_in_cash_and_equivalents"),
            change_in_other_operating_assets_and_liabilities_net=d.get(
                "change_in_other_operating_assets_and_liabilities_net"
            ),
            cik=d.get("cik"),
            depreciation_depletion_and_amortization=d.get(
                "depreciation_depletion_and_amortization"
            ),
            dividends=d.get("dividends"),
            effect_of_currency_exchange_rate=d.get("effect_of_currency_exchange_rate"),
            filing_date=d.get("filing_date"),
            fiscal_quarter=d.get("fiscal_quarter"),
            fiscal_year=d.get("fiscal_year"),
            income_loss_from_discontinued_operations=d.get(
                "income_loss_from_discontinued_operations"
            ),
            long_term_debt_issuances_repayments=d.get(
                "long_term_debt_issuances_repayments"
            ),
            net_cash_from_financing_activities=d.get(
                "net_cash_from_financing_activities"
            ),
            net_cash_from_financing_activities_continuing_operations=d.get(
                "net_cash_from_financing_activities_continuing_operations"
            ),
            net_cash_from_financing_activities_discontinued_operations=d.get(
                "net_cash_from_financing_activities_discontinued_operations"
            ),
            net_cash_from_investing_activities=d.get(
                "net_cash_from_investing_activities"
            ),
            net_cash_from_investing_activities_continuing_operations=d.get(
                "net_cash_from_investing_activities_continuing_operations"
            ),
            net_cash_from_investing_activities_discontinued_operations=d.get(
                "net_cash_from_investing_activities_discontinued_operations"
            ),
            net_cash_from_operating_activities=d.get(
                "net_cash_from_operating_activities"
            ),
            net_cash_from_operating_activities_discontinued_operations=d.get(
                "net_cash_from_operating_activities_discontinued_operations"
            ),
            net_income=d.get("net_income"),
            noncontrolling_interests=d.get("noncontrolling_interests"),
            other_cash_adjustments=d.get("other_cash_adjustments"),
            other_financing_activities=d.get("other_financing_activities"),
            other_investing_activities=d.get("other_investing_activities"),
            other_operating_activities=d.get("other_operating_activities"),
            period_end=d.get("period_end"),
            purchase_of_property_plant_and_equipment=d.get(
                "purchase_of_property_plant_and_equipment"
            ),
            sale_of_property_plant_and_equipment=d.get(
                "sale_of_property_plant_and_equipment"
            ),
            short_term_debt_issuances_repayments=d.get(
                "short_term_debt_issuances_repayments"
            ),
            tickers=d.get("tickers"),
            timeframe=d.get("timeframe"),
        )


@modelclass
class FinancialIncomeStatement:
    basic_earnings_per_share: Optional[float] = None
    basic_shares_outstanding: Optional[float] = None
    cik: Optional[str] = None
    consolidated_net_income_loss: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    depreciation_depletion_amortization: Optional[float] = None
    diluted_earnings_per_share: Optional[float] = None
    diluted_shares_outstanding: Optional[float] = None
    discontinued_operations: Optional[float] = None
    ebitda: Optional[float] = None
    equity_in_affiliates: Optional[float] = None
    extraordinary_items: Optional[float] = None
    filing_date: Optional[str] = None
    fiscal_quarter: Optional[float] = None
    fiscal_year: Optional[float] = None
    gross_profit: Optional[float] = None
    income_before_income_taxes: Optional[float] = None
    income_taxes: Optional[float] = None
    interest_expense: Optional[float] = None
    interest_income: Optional[float] = None
    net_income_loss_attributable_common_shareholders: Optional[float] = None
    noncontrolling_interest: Optional[float] = None
    operating_income: Optional[float] = None
    other_income_expense: Optional[float] = None
    other_operating_expenses: Optional[float] = None
    period_end: Optional[str] = None
    preferred_stock_dividends_declared: Optional[float] = None
    research_development: Optional[float] = None
    revenue: Optional[float] = None
    selling_general_administrative: Optional[float] = None
    tickers: Optional[List[str]] = None
    timeframe: Optional[str] = None
    total_operating_expenses: Optional[float] = None
    total_other_income_expense: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return FinancialIncomeStatement(
            basic_earnings_per_share=d.get("basic_earnings_per_share"),
            basic_shares_outstanding=d.get("basic_shares_outstanding"),
            cik=d.get("cik"),
            consolidated_net_income_loss=d.get("consolidated_net_income_loss"),
            cost_of_revenue=d.get("cost_of_revenue"),
            depreciation_depletion_amortization=d.get(
                "depreciation_depletion_amortization"
            ),
            diluted_earnings_per_share=d.get("diluted_earnings_per_share"),
            diluted_shares_outstanding=d.get("diluted_shares_outstanding"),
            discontinued_operations=d.get("discontinued_operations"),
            ebitda=d.get("ebitda"),
            equity_in_affiliates=d.get("equity_in_affiliates"),
            extraordinary_items=d.get("extraordinary_items"),
            filing_date=d.get("filing_date"),
            fiscal_quarter=d.get("fiscal_quarter"),
            fiscal_year=d.get("fiscal_year"),
            gross_profit=d.get("gross_profit"),
            income_before_income_taxes=d.get("income_before_income_taxes"),
            income_taxes=d.get("income_taxes"),
            interest_expense=d.get("interest_expense"),
            interest_income=d.get("interest_income"),
            net_income_loss_attributable_common_shareholders=d.get(
                "net_income_loss_attributable_common_shareholders"
            ),
            noncontrolling_interest=d.get("noncontrolling_interest"),
            operating_income=d.get("operating_income"),
            other_income_expense=d.get("other_income_expense"),
            other_operating_expenses=d.get("other_operating_expenses"),
            period_end=d.get("period_end"),
            preferred_stock_dividends_declared=d.get(
                "preferred_stock_dividends_declared"
            ),
            research_development=d.get("research_development"),
            revenue=d.get("revenue"),
            selling_general_administrative=d.get("selling_general_administrative"),
            tickers=d.get("tickers"),
            timeframe=d.get("timeframe"),
            total_operating_expenses=d.get("total_operating_expenses"),
            total_other_income_expense=d.get("total_other_income_expense"),
        )


@modelclass
class FinancialRatio:
    average_volume: Optional[float] = None
    cash: Optional[float] = None
    cik: Optional[str] = None
    current: Optional[float] = None
    date: Optional[str] = None
    debt_to_equity: Optional[float] = None
    dividend_yield: Optional[float] = None
    earnings_per_share: Optional[float] = None
    enterprise_value: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    ev_to_sales: Optional[float] = None
    free_cash_flow: Optional[float] = None
    market_cap: Optional[float] = None
    price: Optional[float] = None
    price_to_book: Optional[float] = None
    price_to_cash_flow: Optional[float] = None
    price_to_earnings: Optional[float] = None
    price_to_free_cash_flow: Optional[float] = None
    price_to_sales: Optional[float] = None
    quick: Optional[float] = None
    return_on_assets: Optional[float] = None
    return_on_equity: Optional[float] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return FinancialRatio(
            average_volume=d.get("average_volume"),
            cash=d.get("cash"),
            cik=d.get("cik"),
            current=d.get("current"),
            date=d.get("date"),
            debt_to_equity=d.get("debt_to_equity"),
            dividend_yield=d.get("dividend_yield"),
            earnings_per_share=d.get("earnings_per_share"),
            enterprise_value=d.get("enterprise_value"),
            ev_to_ebitda=d.get("ev_to_ebitda"),
            ev_to_sales=d.get("ev_to_sales"),
            free_cash_flow=d.get("free_cash_flow"),
            market_cap=d.get("market_cap"),
            price=d.get("price"),
            price_to_book=d.get("price_to_book"),
            price_to_cash_flow=d.get("price_to_cash_flow"),
            price_to_earnings=d.get("price_to_earnings"),
            price_to_free_cash_flow=d.get("price_to_free_cash_flow"),
            price_to_sales=d.get("price_to_sales"),
            quick=d.get("quick"),
            return_on_assets=d.get("return_on_assets"),
            return_on_equity=d.get("return_on_equity"),
            ticker=d.get("ticker"),
        )


@modelclass
class FinancialFloat:
    effective_date: Optional[str] = None
    free_float: Optional[int] = None
    free_float_percent: Optional[float] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return FinancialFloat(
            effective_date=d.get("effective_date"),
            free_float=d.get("free_float"),
            free_float_percent=d.get("free_float_percent"),
            ticker=d.get("ticker"),
        )


@modelclass
class RiskFactor:
    cik: Optional[str] = None
    filing_date: Optional[str] = None
    primary_category: Optional[str] = None
    secondary_category: Optional[str] = None
    supporting_text: Optional[str] = None
    tertiary_category: Optional[str] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return RiskFactor(
            cik=d.get("cik"),
            filing_date=d.get("filing_date"),
            primary_category=d.get("primary_category"),
            secondary_category=d.get("secondary_category"),
            supporting_text=d.get("supporting_text"),
            tertiary_category=d.get("tertiary_category"),
            ticker=d.get("ticker"),
        )


@modelclass
class RiskFactorTaxonomy:
    description: Optional[str] = None
    primary_category: Optional[str] = None
    secondary_category: Optional[str] = None
    taxonomy: Optional[float] = None
    tertiary_category: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return RiskFactorTaxonomy(
            description=d.get("description"),
            primary_category=d.get("primary_category"),
            secondary_category=d.get("secondary_category"),
            taxonomy=d.get("taxonomy"),
            tertiary_category=d.get("tertiary_category"),
        )
