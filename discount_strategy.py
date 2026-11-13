from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
  @abstractmethod
  def apply(self, total: float) -> float:
    pass


class NoDiscount(DiscountStrategy):
  def apply(self, total: float) -> float:
    return total


class PercentageDiscount(DiscountStrategy):
  def __init__(self, percentage: float)-> None:
    self.__percentage = percentage

  def apply(self, total: float) -> float:
    # Takes percentage off the total, e.g., 10% off -> total * 0.9
    return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
  def __init__(self, threshold: float, amount: float)-> None:
    self.__threshold = threshold
    self.__amount = amount
  def apply(self, total: float) -> float:
    # Takes fixed amount off if total meets or exceeds the threshold
    return total - self.__amount if total >= self.__threshold else total

class StudentDiscount(DiscountStrategy):
  def apply(self, total: float) -> float:
   # 15% discount for students
    return total * 0.85  