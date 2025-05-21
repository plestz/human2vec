import numpy as np
import pandas as pd

import random

from faker import Faker
Faker.seed(42)
random.seed(42)

# ---- CONSTANTS ----
NUM_NAMES = 10
NUM_REFERRALS = 10

def generate_names(num_names: int) -> list:
    """
    Generate a list of random names.

    Args:
        num_names - The number of names to generate

    Returns:
        list(names) - A list of random names
    """
    fake = Faker()

    names = set()

    while len(names) < num_names:
        name = fake.name()
        names.add(name)

    return list(names)

def generate_referrals(num_referrals: int, member_names: list) -> list:
    """
    Generate a list of random referrals.

    Args:
        num_referrals - The number of referrals to generate
        member_names - A list of member names to use for generating referrals
        
    Returns:
        list(referrals) - A list of random referrals based on the given member names
    """
    referrals = set()

    with open("data/referral_templates.json", "r") as f:
        referral_templates = pd.read_json(f)['template'].tolist()
    
    while len(referrals) < num_referrals:
        referral_template = random.choice(referral_templates)
        referred_member = random.choice(member_names).split(" ")[0].lower()
        referral = referral_template.format(referred_member = referred_member)

        referrals.add(referral)

    return list(referrals)

if __name__ == '__main__':

    member_names = generate_names(NUM_NAMES)
    referrals = generate_referrals(NUM_REFERRALS, member_names)

    with open('data/member_names.txt', 'w') as f:
        for name in member_names:
            f.write(f"{name}\n")
    
    with open('data/referrals.txt', 'w') as f:
        for referral in referrals:
            f.write(f"{referral}\n")