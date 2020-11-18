import argparse
import time
import sys
# import app
# MANUAL
# In command line navigate to the root directory
# Enter:
# MULTIPLE: python -m {number of profile (default:10)} -q {query, key separate by space}
# SINGLE: python -s {profile's url}
# https://www.linkedin.com/in/duydangpham/?originalSubdomain=vn
# Default save as json
# Optional:
# Save extra CSV file: -o {csv file name (default:crawled_profiles.csv)}
# Save only CSV file - No JSON file: -on {csv file name (default:crawled_profiles.csv)}


# Initialize parser
def parser_init():
    parser = argparse.ArgumentParser(
        prog='LinkedIn Crawler',
        usage='%(prog)s [options]',
        description="Crawl LinkedIn user's profile(s) and store the result as a JSON file",
        allow_abbrev=False)

    # Load Dummies accounts from file
    parser.add_argument('-ac',
                        metavar='accounts file',
                        dest='account',
                        nargs='?',
                        type=argparse.FileType('r'),
                        const='accounts.txt')

    # Multiple
    parser.add_argument('-m', '--multiple',
                        metavar='N',
                        dest='multiple',
                        type=int,
                        nargs='?',  # If no argument detected, using const's value
                        const=10,
                        help='Crawl multiple profile. Followed by number of profiles. Default=10')
    # Search Query
    parser.add_argument('-q', '--query',
                        dest='query',
                        nargs='+',
                        help='Search query for user profile')

    # Single
    parser.add_argument('-s', '--single',
                        metavar='[URL]',
                        dest='single',
                        nargs=1,
                        help='Crawl single profile. Followed by profile\'s url')

    # CSV
    parser.add_argument('-o', '--output',
                        metavar='CSV name',
                        dest='csv',
                        nargs='?',
                        const='data',
                        help='Output a CSV file. Default CSV file name: data.csv')

    # No JSON
    parser.add_argument('-on', '--only',
                        metavar='CSV name',
                        dest='no_json',
                        nargs='?',
                        const='data',
                        help='Output only a CSV file. Default CSV file name: data.csv')

    # Exit
    parser.add_argument('-e', '--exit',
                        dest='exit',
                        action='store_true',
                        help='Save account list then exit the program.')
    return parser


# parser.add_argument('-a', metavar='Auto', help='Auto crawl profile')

def parser_handler(parser, driver):
    args = parser.parse_args()
    if args.exit:
        config.save_account_list()
        print('Exiting programing...')
        driver.quit()
        sys.exit()

    # Handle arguments
    if not (args.multiple or args.single or args.account):
        parser.error('Missing argument. Use:\\n -ac: Load accounts list | -m: Multiple crawl | -s: Single crawl.')
    else:
        # if args.account is not None:
        #     config.load_account(args.account)
        #     # while config.current_quota != 0:
        #     #     print(f'Account: {config.active_account[0]}')
        #     #     print(f'Current quota: {config.current_quota}')
        #     #     config.current_quota -= 1
        #     # config.next_active()
        #     # while config.current_quota != 0:
        #     #     print(f'Account: {config.active_account[0]}')
        #     #     print(f'Current quota: {config.current_quota}')
        #     #     config.current_quota -= 1
        #     # exit(0)
        if args.multiple is not None:
            start_time = time.time()
            # No search query
            if not args.query:
                parser.error('Please input search query after -q or --query')
            search_query = 'site:linkedin.com/in/ '
            for q in args.query:
                search_query = search_query + "AND \"" + q + "\" "
            case = 0
            file_name = config.FILE_NAME_MULTIPLE

            if args.csv:
                file_name = args.csv
                case = 1
            elif args.no_json:
                file_name = args.no_json
                case = 2
            amount = args.multiple
            print(f'Settings: Type: multiple -- Amount: {amount} -- Case: {case} -- File name: {file_name}')
            controller.multiple(search_query, case, amount, file_name, driver)
            print(f'Multiple: {amount} profile(s)')
            print(f'Query time: {controller.query_time} seconds')
            print(f'Total extract data time: {controller.multiple_time}')
            print("Total time: %s seconds" % (time.time() - start_time))

        elif args.single is not None:
            start_time = time.time()
            case = 0
            file_name = config.FILE_NAME_SINGLE

            if args.csv:
                file_name = args.csv
                case = 1
            elif args.no_json:
                file_name = args.no_json
                case = 2
            print(f"Settings: Type: single -- Case: {case} -- File name: {file_name}")
            controller.single(args.single[0], case, file_name, driver)
            print('Single profile')
            print("Total time: %s seconds" % (time.time() - start_time))
        config.update_quota()
