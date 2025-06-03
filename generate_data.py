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


# ---- GENERATE DATA ----
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

def generate_referrals(member_first_names: list, num_referrals: int = None, no_template_reuse: bool = False) -> list:
    """
    Generate a list of random referrals.

    Args:
        member_names - A list of member names to use for generating referrals
        num_referrals - The number of referrals to generate. If None, generate as many as there are templates.
        no_template_reuse - If True, do not reuse referral templates once they have been used
        
    Returns:
        list(referrals) - A list of random template-originating referrals based on the given member names
    """
    referrals = set()

    # Store the mapping of member names to their referrals
    member_to_referrals_received = {name: [] for name in member_first_names}
    
    # Store the mapping of member names to members they referred
    member_to_member_referrals_given = {name: [] for name in member_first_names}

    # Open the set of referral templates to generate from
    with open("data/preprocess/referral_templates.json", "r") as f:
        referral_templates = pd.read_json(f)['template'].tolist()

    # If template reuse is disabled and we have a specified number of referrals, 
    # ensure that the number of referrals does not exceed the number of templates.
    if no_template_reuse and num_referrals is not None:
        assert num_referrals <= len(referral_templates)
    
    # If no number of referrals is specified, use the number of templates
    referrals_to_generate = len(referral_templates) if num_referrals is None else num_referrals

    # Until we have the desired number of unique referrals, generate more
    while len(referrals) < referrals_to_generate:

        referral_template = random.choice(referral_templates)

        # To who is the referral being given?
        referred_member = random.choice(member_first_names)
        # From who is the referral being given?
        non_referred_members = member_first_names.copy()
        non_referred_members.remove(referred_member)
        referring_member = random.choice(non_referred_members)

        referral = referral_template.format(referred_member = referred_member)

        # If the same exact referral has already been generated, skip it
        if referral in referrals:
            continue

        referrals.add(referral)

        # Map each referral-receiving member to the referrals they have received
        member_to_referrals_received[referred_member].append(referral)

        # Map each referring member to the members they have referred
        member_to_member_referrals_given[referring_member].append(referred_member)

        # If we are not reusing templates, remove the template from the list of available templates for future selection
        if no_template_reuse:
            referral_templates.remove(referral_template)

    with open(f"data/process/member_to_referrals_received_{NUM_NAMES}N_{len(referrals)}R{"_NTR" if no_template_reuse else ""}.json", "w") as f:
        json.dump(member_to_referrals_received, f, indent = 4)

    with open(f"data/process/member_to_member_referrals_given_{NUM_NAMES}N_{len(referrals)}R{"_NTR" if no_template_reuse else ""}.json", "w") as f:
        json.dump(member_to_member_referrals_given, f, indent = 4)

    return list(referrals)


# ---- MAIN ----
if __name__ == '__main__':

    member_first_names = generate_first_names(NUM_NAMES)

    ntr_flag = True # no_template_reuse flag

    referrals = generate_referrals(member_first_names, no_template_reuse = ntr_flag)

    # Save distinct member names
    with open(f'data/preprocess/member_first_names_{NUM_NAMES}N_{len(referrals)}R{"_NTR" if ntr_flag else ""}.txt', 'w') as f:
        for name in member_first_names:
            f.write(f"{name}\n")
    
    # Save distinct referrals
    with open(f'data/preprocess/referrals_{NUM_NAMES}N_{len(referrals)}R{"_NTR" if ntr_flag else ""}.txt', 'w') as f:
        for referral in referrals:
            f.write(f"{referral}\n")