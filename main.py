import streamlit as st

def main_page():
    options = ['Qualifying Bet', 'Free Bet']
    st.title('Matched Betting Calculator')
    selected_option = st.radio('Select Bet Type', options)
    print(f"Selected option: {selected_option}")
    bet_window(selected_option)

def submission_check(back_comms, back_odds_decimal, back_stake_input, lay_comms, lay_odds_decimal):
    print(f"Initial values - back_comms: {back_comms}, back_odds_decimal: {back_odds_decimal}, back_stake_input: {back_stake_input}, lay_comms: {lay_comms}, lay_odds_decimal: {lay_odds_decimal}")
    if back_comms:
        print("back comms - truthy value")
    if not back_comms:
        back_comms = 0
        print("back comms is a falsy value so i default to zero") # confirmed defaults to zero
    if not lay_comms:
        lay_comms = 0
        print("lay comms is a falsy value so i default to zero")
    if not back_odds_decimal or not back_stake_input or not lay_odds_decimal:
        print("One or more required inputs are missing")
        return False
    print("All required inputs are present")
    return True

def bet_window(bet_type):
    print(f"Bet type: {bet_type}")
    st.subheader(bet_type)
    st.markdown("##### Back Bet")
    col1, col2 = st.columns(2)
    with col1:
        back_stake_input = st.number_input('Back Stake', placeholder='Amount to bet (£)')
        print(f"Back Stake Input: {back_stake_input}")
        back_comms = st.number_input('Back Commission (%) ', placeholder='Defaults to 0%')
        print(f"Back Commission: {back_comms}")

    with col2:
        back_odds_decimal = st.number_input(label='Back Odds (In Decimal)')
        print(f"Back Odds Decimal: {back_odds_decimal}")
    st.divider()
    st.markdown("##### Lay Bet")

    lay_col1, lay_col2 = st.columns(2)
    with lay_col1:
        lay_odds_decimal = st.number_input(label='Lay Odds (In Decimal)')
        print(f"Lay Odds Decimal: {lay_odds_decimal}")
    with lay_col2:
        lay_comms = st.number_input('Lay Commission (%) ', placeholder='Defaults to 0%')
        print(f"Lay Commission: {lay_comms}")
    
    if submission_check(back_comms, back_odds_decimal, back_stake_input, lay_comms, lay_odds_decimal):
        current_bet = Bet(back_stake_input, back_odds_decimal, lay_comms, back_comms, lay_odds_decimal, bet_type)
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('##### Lay Stake Required')
            lay_stake = current_bet.get_lay_stake()
            print(f"Lay Stake Needed: {lay_stake}")
            st.write(lay_stake)

        with col2:
            st.markdown('##### Lay Liability')
            lay_liability = current_bet.get_lay_liability()
            print(f"Lay Liability: {lay_liability}")
            st.write(lay_liability)

        with col3:
            st.markdown('##### Profit if Back Wins')
            profit_back_win = current_bet.get_case_back_bet_win()
            print(f"Profit if Back Wins: {profit_back_win}")
            st.write(profit_back_win)
        with col4:
            st.markdown('##### Profit if Lay Wins')
            profit_lay_win = current_bet.get_case_lay_bet_wins()
            print(f"Profit if Lay Wins: {profit_lay_win}")
            st.write(profit_lay_win)

class Bet:
    def __init__(self, back_stake, back_odds, lay_commission, back_commission, lay_odds, bet_type):
        self.back_stake = back_stake  # 10
        self.back_odds = back_odds # 3.4
        self.lay_commission = lay_commission # 0.02 or 0
        self.back_commission = back_commission # 0.02 or 0
        self.lay_odds = lay_odds # 4.0
        self.bet_type = bet_type # FREE or QUALIFYING
        print(f"Initialized Bet: {self.__dict__}")

    def get_lay_stake(self): # 8.5
        if self.bet_type == "Qualifying Bet":
            lay_stake = round((self.back_stake * self.back_odds) / self.lay_odds, 2)
            print(f"Calculated Lay Stake: {lay_stake}")
            return lay_stake
        print("Free Bet Lay Stake")
        return round(self.back_stake * (self.back_odds - 1) / self.lay_odds, 2)

    def get_lay_liability(self):
        lay_liability = round(self.get_lay_stake() * (self.lay_odds - 1), 2)
        print(f"Calculated Lay Liability: {lay_liability}")
        return lay_liability



    def get_case_back_bet_win(self):  # Profit calculation for back bet
        # Calculate the potential winnings from the back bet
        back_winnings = self.back_stake * (self.back_odds - 1)  # 10 * (3.4 - 1) = 24
        print(f"Initial Back Winnings: {back_winnings}")
        print("Back Commission", self.back_commission)
        print("lay", self.get_lay_liability())
        
        # If it's a free bet, there's no back stake, so we just calculate winnings

        if self.bet_type == "Free Bet":
            back_winnings -= back_winnings * self.back_commission  # Apply commission
            # back_winnings = 24
            print(f"Back Winnings after Commission (Free Bet): {back_winnings}")
            return round(back_winnings - self.get_lay_liability(), 2)

        # QUALIFYING
        # apply the commission and subtract the back stake
        back_winnings -= back_winnings * self.back_commission  # 24 - (24 * 0.02) = 23.52
        print(f"Back Winnings after Commission (Qualifying Bet): {back_winnings}")
        profit = round(back_winnings - self.get_lay_liability(), 2)  # 23.52 - 25.5 = -1.98
        print(f"Profit if Back Bet Wins: {profit}")
        return profit

    def get_case_lay_bet_wins(self):
        # Profit calculation when the lay bet wins
        lay_winnings = self.get_lay_stake()  # Amount won from the lay bet
        print(f"Initial Lay Winnings: {lay_winnings}")

        lay_commission_deduction = self.lay_commission * (self.get_lay_stake() * (self.lay_odds - 1))
        print(f"Lay Commission Deduction: {lay_commission_deduction}")

        if self.bet_type == "Free Bet":
            # For free bets, there's no back stake to subtract
            profit = round(lay_winnings - lay_commission_deduction, 2)
            print(f"Profit if Lay Bet Wins (Free Bet): {profit}")
            return profit
        else:
            # Subtract the back stake for qualifying bets
            profit = round(lay_winnings - lay_commission_deduction - self.back_stake, 2)
            print(f"Profit if Lay Bet Wins (Qualifying Bet): {profit}")
            return profit

if __name__ == "__main__":
    main_page()