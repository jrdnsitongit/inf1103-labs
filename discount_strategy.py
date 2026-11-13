from abc import ABC, abstractmethod

def _validate_non_negative_number(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be a number.")
    val = float(value)
    if val < 0:
        raise ValueError(f"{field_name} cannot be negative.")
    return val

class DiscountStrategy(ABC):
  @abstractmethod
  def apply(self, total: float) -> float:
    pass


class NoDiscount(DiscountStrategy):
  def apply(self, total: float) -> float:
    return _validate_non_negative_number(total, "Total")


class PercentageDiscount(DiscountStrategy):
  def __init__(self, percentage: float) -> None:
      pct = _validate_non_negative_number(percentage, "Percentage")
      if pct > 100:
          raise ValueError("Percentage cannot exceed 100.")
      self.__percentage = pct

  def apply(self, total: float) -> float:
    # Takes percentage off the total, e.g., 10% off -> total * 0.9
    return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
  def __init__(self, threshold: float, amount: float) -> None:
    self.__threshold = _validate_non_negative_number(threshold, "Threshold")
    self.__amount = _validate_non_negative_number(amount, "Discount amount")

  def apply(self, total: float) -> float:
     valid_total = _validate_non_negative_number(total, "Total")
     if valid_total >= self.__threshold:
         return max(0.0, valid_total - self.__amount)
     return valid_total


class StudentDiscount(DiscountStrategy):
  def apply(self, total: float) -> float:
      valid_total = _validate_non_negative_number(total, "Total")
        #15% off for students
      return valid_total * 0.85