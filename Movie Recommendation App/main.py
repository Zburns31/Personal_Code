



if __name__ == '__main__':

    print("Welcome! Thanks for using Zac's Movie Recommendation App. To begin, enter one of the following options: ")
    print('1: Popularity Based Recommendations')
    print('2: Content Based Recommendation - This will find movies which are similar to your provided input')
    print('3: User Based Recommendations - This will find movies which are similar to Users like you')
    print('4: Hybrid Based Recommendations. - These recommendations will be a combination of the above options')


    user_input = input('Please enter your choice:')

    try:
        selection = int(user_input)
    except:
        ValueError(f'Your selection needs to be an Integer. {selection} is not an integer')

    # https://maciejkula.github.io/spotlight/datasets/movielens.html
    # https://conx.readthedocs.io/en/latest/RecommendingMovies.html#Designing-the-Dataset
    