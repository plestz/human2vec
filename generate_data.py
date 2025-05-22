import numpy as np
import pandas as pd

import random
import json

from faker import Faker
Faker.seed(42)
random.seed(42)

# ---- CONSTANTS ----
NUM_NAMES = 75
NUM_REFERRALS = 10000

def generate_first_names(num_names: int) -> list:
    """
    Generate a list of random names.

    Args:
        num_names - The number of names to generate

    Returns:
        list(names) - A list of random names
    """
    fake = Faker()

    first_names = set()

    # Until we have the desired number of unique names, generate more
    while len(first_names) < num_names:
        name = fake.name().split(" ")[0].lower()
        first_names.add(name)

    return list(first_names)

def generate_referrals(num_referrals: int, member_first_names: list) -> list:
    """
    Generate a list of random referrals.

    Args:
        num_referrals - The number of referrals to generate
        member_names - A list of member names to use for generating referrals
        
    Returns:
        list(referrals) - A list of random referrals based on the given member names
    """
    referrals = set()

    # Store the mapping of member names to their referrals
    member_to_referrals = {name: [] for name in member_first_names}

    # Open the set of referral templates to generate from
    with open("data/preprocess/referral_templates.json", "r") as f:
        referral_templates = pd.read_json(f)['template'].tolist()
    
    # Until we have the desired number of unique referrals, generate more
    while len(referrals) < num_referrals:

        referral_template = random.choice(referral_templates)
        referred_member = random.choice(member_first_names)
        referral = referral_template.format(referred_member = referred_member)

        referrals.add(referral) # Sets force uniqueness!!!

        if referral not in member_to_referrals[referred_member]:
            member_to_referrals[referred_member].append(referral)

    with open("data/process/member_to_referrals.json", "w") as f:
        json.dump(member_to_referrals, f, indent = 4)

    return list(referrals)

if __name__ == '__main__':

    member_first_names = generate_first_names(NUM_NAMES)
    referrals = generate_referrals(NUM_REFERRALS, member_first_names)

    # Save distinct member names
    with open('data/preprocess/member_first_names.txt', 'w') as f:
        for name in member_first_names:
            f.write(f"{name}\n")
    
    # Save distinct referrals
    with open('data/preprocess/referrals.txt', 'w') as f:
        for referral in referrals:
            f.write(f"{referral}\n")