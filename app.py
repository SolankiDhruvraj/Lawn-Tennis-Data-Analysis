from flask import Flask, render_template,request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

app = Flask(__name__)

data_2000 = pd.read_excel('atp_2000.xls')
data_2001 = pd.read_excel('atp_2001.xls')
data_2002 = pd.read_excel('atp_2002.xls')
data_2003 = pd.read_excel('atp_2003.xls')
data_2004 = pd.read_excel('atp_2004.xls')
data_2005 = pd.read_excel('atp_2005.xls')
data_2006 = pd.read_excel('atp_2006.xls')
data_2007 = pd.read_excel('atp_2007.xls')
data_2008 = pd.read_excel('atp_2008.xls')
data_2009 = pd.read_excel('atp_2009.xls')
data_2010 = pd.read_excel('atp_2010.xls')
data_2011 = pd.read_excel('atp_2011.xls')
data_2012 = pd.read_excel('atp_2012.xls')
data_2013 = pd.read_excel('atp_2013.xlsx')
data_2014 = pd.read_excel('atp_2014.xlsx')
data_2015 = pd.read_excel('atp_2015.xlsx')
data_2016 = pd.read_excel('atp_2016.xlsx')
data_2017 = pd.read_excel('atp_2017.xlsx')
data_2018 = pd.read_excel('atp_2018.xlsx')
data_2019 = pd.read_excel('atp_2019.xlsx')
data_2020 = pd.read_excel('atp_2020.xlsx')
data_2021 = pd.read_excel('atp_2021.xlsx')
data_2022 = pd.read_excel('atp_2022.xlsx')
data_2023 = pd.read_excel('atp_2023.xlsx')

@app.route('/',methods=['GET','POST'])
def index():
    data = None
    if request.method == 'POST':
        selected_year = request.form['year']
        if selected_year == '2001':
            data = data_2001
        elif selected_year == '2002':
            data = data_2002
        elif selected_year == '2003':
            data = data_2003
        elif selected_year == '2004':
            data = data_2004
        elif selected_year == '2005':
            data = data_2005
        elif selected_year == '2006':
            data = data_2006
        elif selected_year == '2007':
            data = data_2007
        elif selected_year == '2008':
            data = data_2008
        elif selected_year == '2009':
            data = data_2009
        elif selected_year == '2010':
            data = data_2010
        elif selected_year == '2011':
            data = data_2011
        elif selected_year == '2012':
            data = data_2012
        elif selected_year == '2013':
            data = data_2013
        elif selected_year == '2014':
            data = data_2014
        elif selected_year == '2015':
            data = data_2015
        elif selected_year == '2016':
            data = data_2016
        elif selected_year == '2017':
            data = data_2017
        elif selected_year == '2018':
            data = data_2018
        elif selected_year == '2019':
            data = data_2019
        elif selected_year == '2020':
            data = data_2020
        elif selected_year == '2021':
            data = data_2021
        elif selected_year == '2022':
            data = data_2022
        elif selected_year == '2023':
            data = data_2023
        
    if data is None:
        error_message = "Invalid year selected"
        return render_template('index.html', error=error_message, plot_urls=[], titles=[])

    plot_urls = []
    titles = []

    series_counts = data['Series'].value_counts()

# Create a pie chart to visualize the tournament series distribution
    plt.figure(figsize=(6, 4))
    plt.pie(series_counts, labels=series_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Tournament Series Distribution')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close() 
    plot_urls.append(plot_url)
    titles.append('Tournament Series Distribution')

    surface_counts = data['Surface'].value_counts()

# Create a bar plot to visualize the tournament surface distribution
    plt.figure(figsize=(6, 4))
    plt.bar(surface_counts.index, surface_counts.values)
    plt.title('Tournament Surface Distribution')
    plt.xlabel('Surface')
    plt.ylabel('Count')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close() 
    plot_urls.append(plot_url)
    titles.append('Tournament Surface Distribution')

    # Visualize first set wins
    first_set_wins = data.groupby('Winner')['W1'].sum().reset_index()
    first_set_wins = first_set_wins.rename(columns={'W1': 'FirstSetWins'})
    plt.figure(figsize=(6, 4))
    sns.barplot(x='FirstSetWins', y='Winner', data=first_set_wins.head(10))
    plt.title('Top Players with Most First Set Wins')
    plt.xlabel('Number of First Set Wins')
    plt.ylabel('Player')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plot_urls.append(plot_url)
    titles.append('Top Players with Most First Set Wins')

  
    total_wins = data['Winner'].value_counts().reset_index()
    total_wins.columns = ['Player', 'TotalWins']

    top_player_total_wins = total_wins.loc[total_wins['TotalWins'].idxmax()]

    # Create a line plot to visualize the top player with total wins
    plt.figure(figsize=(6, 4))
    plt.plot(total_wins['Player'].head(10), total_wins['TotalWins'].head(10), marker='o', linestyle='-')
    plt.title('Top Players with Most Total Wins')
    plt.xlabel('Player')
    plt.ylabel('Number of Total Wins')
    plt.xticks(rotation=45) 
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()  
    plot_urls.append(plot_url)
    titles.append(f'Top Players with Most Total Wins in {selected_year}')


    # Visualize wins in straight sets
    total_wins = data['Winner'].value_counts().reset_index()
    total_wins.columns = ['Player', 'TotalWins']

    top_player_total_wins = total_wins.loc[total_wins['TotalWins'].idxmax()]

    # Create a bar plot to visualize the top player with total wins
    plt.figure(figsize=(6, 4))
    sns.barplot(x='TotalWins', y='Player', data=total_wins.head(10))
    plt.title('Top Players with Most Total Wins')
    plt.xlabel('Number of Total Wins')
    plt.ylabel('Player')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()  
    plot_urls.append(plot_url)
    titles.append('Top Players with Most Total Wins')


    # Visualize wins with higher rank
    straight_sets_wins = data[data['Wsets'] == 2]
    straight_sets_wins_count = straight_sets_wins['Winner'].value_counts().reset_index()
    straight_sets_wins_count.columns = ['Player', 'StraightSetsWins']

    top_player_straight_sets_wins = straight_sets_wins_count.loc[straight_sets_wins_count['StraightSetsWins'].idxmax()]

    # Create a bar plot to visualize the top player with wins in straight sets
    plt.figure(figsize=(6, 4))
    sns.barplot(x='StraightSetsWins', y='Player', data=straight_sets_wins_count.head(10))
    plt.title('Top Players with Most Wins in Straight Sets')
    plt.xlabel('Number of Wins in Straight Sets')
    plt.ylabel('Player')

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()  
    plot_urls.append(plot_url)
    titles.append('Top Players with Most Wins in Straight Sets')


    # Visualize rank vs. points
    higher_rank_wins = data[data['WRank'] < data['LRank']]

    higher_rank_wins_count = higher_rank_wins['Winner'].value_counts().reset_index()
    higher_rank_wins_count.columns = ['Player', 'HigherRankWins']


    higher_rank_wins = data[data['WRank'] < data['LRank']]

    players_lost_to_higher_rank = higher_rank_wins['Loser'].tolist()

    plt.figure(figsize=(6, 4))
    plt.pie([len(players_lost_to_higher_rank), len(data) - len(players_lost_to_higher_rank)],
            labels=['Lost to Higher Rank', 'Other Matches'],
            autopct='%1.1f%%',
            colors=['lightcoral', 'lightblue'])
    plt.title('Distribution of Players Who Lost to Higher Ranked Players')

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    plot_urls.append(plot_url)
    titles.append('Distribution of Players Who Lost to Higher Ranked Players')

    # Count the number of matches for each Comment type
    comment_counts = data['Comment'].value_counts().reset_index()
    comment_counts.columns = ['Comment Type', 'Match Count']

    # Create a pie chart to visualize Comment counts
    plt.figure(figsize=(6, 4))
    plt.pie(comment_counts['Match Count'], labels=comment_counts['Comment Type'], autopct='%1.1f%%')
    plt.title('Distribution of Match Comment Types')
    plt.axis('equal')  # Equal aspect ratio ensures a circular pie chart

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()  # Close the plot to release resources

    # Append the plot URL and title to the appropriate lists
    plot_urls.append(plot_url)
    titles.append('Distribution of Match Comment Types')

    # Wins on different surfaces
    surface_wins = data.groupby(['Surface', 'Winner'])['Winner'].count().reset_index(name='Wins')
    surface_wins_pivot = surface_wins.pivot(index='Winner', columns='Surface', values='Wins')
    surface_wins_pivot.fillna(0, inplace=True)

    surface_wins_pivot['Total'] = surface_wins_pivot.sum(axis=1)
    surface_wins_pivot = surface_wins_pivot.sort_values('Total', ascending=False)
    surface_wins_pivot.drop('Total', axis=1, inplace=True)

    # Create a grouped bar chart
    plt.figure(figsize=(20, 8))
    width = 0.2
    x = range(len(surface_wins_pivot))

    for i, surface in enumerate(['Hard', 'Clay', 'Grass']):
        plt.bar([pos + width * i for pos in x], surface_wins_pivot[surface], width=width, label=surface)

    plt.title('Players with Most Wins on Different Surfaces')
    plt.xlabel('Player')
    plt.ylabel('Wins')
    plt.xticks([pos + width for pos in x], surface_wins_pivot.index, rotation='vertical')
    plt.legend(title='Surface', loc='upper right')
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()  

    plot_urls.append(plot_url)
    titles.append('Players with Most Wins on Different Surfaces')


    return render_template('index.html', plot_urls=plot_urls, titles=titles)

if __name__ == '__main__':
    app.run(debug=True)
