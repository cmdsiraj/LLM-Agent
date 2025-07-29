def calculate_startup_costs():
     # Cost assumptions (in USD)\n    
     # # MVP Development: Estimated hours for a small team or agency\n    
    development_hours = 800  # Approx. 4-5 months for a small team\n    
    blended_hourly_rate = 75  # A mix of senior/junior talent\n    
    development_cost = development_hours * blended_hourly_rate
    # Initial Marketing: Focused on a single city launch\n    # Digital ads, local influencer outreach, launch events\n    
    initial_marketing_budget = 15000
    # Infrastructure: Cloud services (e.g., AWS, Azure) for the first 6 months\n    
    monthly_infra_cost = 500
    first_6_months_infra_cost = monthly_infra_cost * 6
    # Legal & Administrative: Business registration, basic contracts\n    
    legal_admin_cost = 2500
    # Calculate sub-total\n    
    sub_total = development_cost + initial_marketing_budget + first_6_months_infra_cost + legal_admin_cost
    # Contingency Fund: For unexpected expenses (always recommended)\n    
    contingency_percentage = 0.15  # 15%\n    
    contingency_fund = sub_total * contingency_percentage
    # Total Estimated Cost\n    
    total_cost = sub_total + contingency_fund
    # Print the formatted results\n    
    print("--- GigSync: Preliminary Launch Cost Estimate ---")
    print(f"1. MVP Development:       ${development_cost:,.2f} ({development_hours} hours @ ${blended_hourly_rate}/hr)")
    print(f"2. Initial Marketing:       ${initial_marketing_budget:,.2f} (First city launch)\")\n    print(f\"3. 6-Month Infrastructure:  ${first_6_months_infra_cost:,.2f}")
    print(f"4. Legal & Admin:           ${legal_admin_cost:,.2f}\")\n    print(\"--------------------------------------------------")    
    print(f"Sub-Total:                ${sub_total:,.2f}\")\n    print(f\"Contingency (15%):        ${contingency_fund:,.2f}")   
    print("--------------------------------------------------\")\n    print(f\"TOTAL ESTIMATED LAUNCH COST: ${total_cost:,.2f}")

calculate_startup_costs()
