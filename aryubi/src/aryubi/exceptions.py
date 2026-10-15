"""Custom exceptions for Aryubi finance agent."""


class AryubiError(Exception):
    """Base exception for Aryubi errors."""


class BudgetError(AryubiError):
    """Raised when budget input is invalid."""


class CashflowError(AryubiError):
    """Raised when cashflow input is invalid."""


class ProfitError(AryubiError):
    """Raised when P&L input is invalid."""


class InvestmentError(AryubiError):
    """Raised when investment computation input is invalid."""


class AnalysisError(AryubiError):
    """Raised when general finance report fails."""


class ConfigurationError(AryubiError):
    """Raised when configuration is invalid."""
