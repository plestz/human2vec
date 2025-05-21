import numpy as np
import pandas as pd

import random

from faker import Faker
Faker.seed(42)
random.seed(42)

def generate_names(num_names: int) -> list:
    """
    Generate a list of random names.
    """
    fake = Faker()
    names = list({fake.name() for _ in range(num_names * 3)}) # Generate extra in case of duplicates
    return names[:num_names]

def generate_referrals(num_referrals: int) -> list:
    """
    Generate a list of random referrals.
    """
    referrals = set()

    

    return referrals[:num_referrals]

if __name__ == '__main__':

    num_names = 10
    member_names = generate_names(num_names)
    print(member_names)