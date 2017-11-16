from selenium import webdriver
from selenium.webdriver.support.ui import Select
from Professor import *
import time
import re
import threading
import datetime
import os


class ProfessorParser:

    def __init__(self, num_threads):
        '''
        Default constructor for python, initializes all variables for the class item
        :param num_threads: The number of threads that need to be spawned.
        class items:
            numThreads: The number of threads in the class item
            all_data: An array that will be used to store all of the data retrieved by each thread
            num_options: The total number of pages that need to be accessed.
            all_threads: An array that will be used to store information on all of the threads.
            meta_data: A file that will store the metadata about runtime information.
        :return:
        '''
        self.num_threads = num_threads
        self.all_data = []
        self.num_options = 0
        for i in range(num_threads):
            self.all_data.append([])
        self.all_threads = []
        filename = "runTimeInfo.txt"
        if os.path.exists(filename):
            self.meta_data = open(filename, 'a')
        else:
            self.meta_data = open(filename, 'w')

    def getNumOptions(self):
        '''
        retrieves the number of options from the web page and stores the information in self.num_options
        '''
        COptions = webdriver.ChromeOptions()
        COptions.add_argument('headless')
        driver = webdriver.Chrome("/Users/boazcogan/Downloads/chromedriver", chrome_options=COptions)
        driver.get("https://ldaps.sonoma.edu/fasd/")
        drop_down = driver.find_element_by_id("dept")
        total_options = len(Select(drop_down).options)-1
        self.num_options = total_options
        driver.close()

    def spawnThreads(self):
        '''
        Spawns a number of threads and evenly divides the amount of work that they have to do between them. Note
        that each thread is designated an array to pass the result of its work into. Each thread is stored into
        self.all_threads.
        '''

        self.getNumOptions()
        start = int(self.num_options // self.num_threads)
        for i in range(self.num_threads):
            t_start = i * start + 1
            t_end = (i+1)*start
            if i == (self.num_threads - 1):
                t_end = self.num_options
            b = threading.Thread(target=self.getProfessorFromPages, args=(t_start, t_end, i))
            b.start()
            self.all_threads.append(b)

    def timeIt(self):
        '''
        controls the timing of the program and writing of the data and metadata. Checks for thread completion by
        the status in their str converted selves.
        :return nothing
        '''
        now = datetime.datetime.now()
        self.meta_data.write("Now displaying runtime information for: " + str(now) + '\n')
        self.meta_data.write("Retrieving information using " + str(self.num_threads) + " threads.\n")
        start_time = time.time()
        num_complete = 0
        while True:
            for i in range(len(self.all_threads)):
                if "stopped" in str(self.all_threads[i]):
                    num_complete += 1
                if num_complete == self.num_threads:
                    end_time = time.time()
                    self.meta_data.write("the total time for all threads is: " + str((end_time - start_time) / 60) +
                                         " minutes.\n\n")
                    self.writeAllData()
                    return
            num_complete = 0

    def writeAllData(self):
        '''
        Write all of the data from the arrays to a file. This is done after thread completion
        '''
        filename = open("threadingData.txt", "w")
        filename.write("{\n    Employees :\n    [\n")
        for j in range(len(self.all_data)):
            for i in range(len(self.all_data[j])):
                if self.all_data[j][i] != self.all_data[-1][-1]:
                    self.all_data[j][i].write_Professor(filename)
                else:
                    self.all_data[j][i].write_last_Professor(filename)
        filename.write("    ]\n}")

    def getProfessorFromPages(self, start, end, thread_num):
        '''
        Uses the Selenium module to grab professor information from SSU's directory web page. Each thread is only
        responsible for retrieving the data from its own page and only writes its data to the thread_num'th item in
        the parent class's all_data array.
        :param start: the first item in the drop down list to access.
        :param end: the last item in the drop down list to access.
        :param thread_num: the value of all data to add information to.
        :return:
        '''
        f_start = start
        beginning_of_thread = time.time()
        this_threads_data = self.all_data[thread_num]
        finished = False
        COptions = webdriver.ChromeOptions()
        COptions.add_argument('headless')
        driver = webdriver.Chrome("/Users/boazcogan/Downloads/chromedriver", chrome_options=COptions)
        # while there are still pages that have not been accessed within the range start:end.
        while not finished:
            driver.get("https://ldaps.sonoma.edu/fasd/")
            drop_down = driver.find_element_by_id("dept")
            options = Select(drop_down)
            options.select_by_visible_text(options.options[start].text)
            driver.find_element_by_xpath('//*[@id="main-content-body"]/form/fieldset/div[3]/input[1]').click()
            results = driver.find_element_by_id("results")
            # if there were results
            if not("Your search term(s) returned no results." in results.text):
                results2 = driver.find_element_by_class_name("stripeMe")
                links = results2.find_elements_by_partial_link_text(",")
                # re-access the items to avoid stale elements and select each faculty information page.
                for i in range(len(links)):
                    results2 = driver.find_element_by_class_name("stripeMe")
                    links = results2.find_elements_by_partial_link_text(",")
                    links[i].click()
                    information = driver.find_elements_by_tag_name("tr")
                    all_information = []
                    # access all of the information on the faculty page.
                    for j in range(len(information)):
                        all_information.append(re.sub(r".*:", "", information[j].text))
                    this_threads_data.append(Professor(all_information[0][1:], all_information[1][1:],
                                                       all_information[2][1:], all_information[3][1:],
                                                       all_information[4][1:], all_information[5][1:],
                                                       all_information[6][1:], all_information[7][1:]))
                    this_threads_data[-1].clean_phone_number()
                    this_threads_data[-1].fix_name()
                    driver.back()
            start += 1
            if start > end:
                finished = True
        driver.close()
        end_of_thread = time.time()
        self.meta_data.write("Thread: " + str(thread_num) + " gathering information on pages: " + str(f_start) + "," +
                             str(end) + " has taken " + str(round(((end_of_thread-beginning_of_thread)/60), 2)) +
                             " minutes.\n")
