# Core Pkg
import streamlit as st 
import streamlit.components.v1 as stc
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
from openai import OpenAI
import random



# Load EDA
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel


# Load Our Dataset
def load_data(data):
	df = pd.read_csv(data)
	return df 


# Fxn
# Vectorize + Cosine Similarity Matrix

def vectorize_text_to_cosine_mat(data):
	count_vect = CountVectorizer()
	cv_mat = count_vect.fit_transform(data)
	# Get the cosine
	cosine_sim_mat = cosine_similarity(cv_mat)
	return cosine_sim_mat



# Recommendation Sys
@st.cache
def get_recommendation(title,cosine_sim_mat,df,num_of_rec=10):
	# indices of the course
	course_indices = pd.Series(df.index,index=df['course_title']).drop_duplicates()
	# Index of course
	idx = course_indices[title]

	# Look into the cosine matr for that index
	sim_scores =list(enumerate(cosine_sim_mat[idx]))
	sim_scores = sorted(sim_scores,key=lambda x: x[1],reverse=True)
	selected_course_indices = [i[0] for i in sim_scores[1:]]
	selected_course_scores = [i[0] for i in sim_scores[1:]]

	# Get the dataframe & title
	result_df = df.iloc[selected_course_indices]
	result_df['similarity_score'] = selected_course_scores
	final_recommended_courses = result_df[['Course Name','similarity_score','url']]
	return final_recommended_courses.head(num_of_rec)


RESULT_TEMP = """
<div style="width:90%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 60px;
box-shadow:0 0 15px 5px #ccc; background-color: #a8f0c6;
  border-left: 5px solid #6c6c6c;">
<h4>{}</h4>
<p style="color:blue;"><span style="color:black;">📈Score::</span>{}</p>
<p style="color:blue;"><span style="color:black;">🔗</span><a href="{}",target="_blank">Link</a></p>
<p style="color:blue;"><span style="color:black;">💲Price:</span>{}</p>
<p style="color:blue;"><span style="color:black;">🧑‍🎓👨🏽‍🎓 Students:</span>{}</p>

</div>
"""

# Search For Course 

def search_term_if_not_found(term,df):
	result_df = df[df['Course Name'].str.contains(term)]
	return result_df


def main():

	with st.sidebar:
		selected= option_menu(
			menu_title="Menu",
			options=["Home","Consistency","courserecommendation","Learn","Doubtclearance","Contact"]
			)

	df = load_data("Coursera.csv")

	if selected == "Home":
		st.title("Welcome to Our Learning Platform!")
		st.write("""
    ## About Us
    In today's digital age, the abundance of information can make finding the right course or learning path overwhelming. We aim to cut through the noise by leveraging advanced algorithms to provide personalized guidance, helping you navigate the vast sea of educational opportunities by offering tailored roadmaps, which helps not only in efficient learning but also unlocks more opportunities aligned with your interests and career goals.
		   

    Our learning platform aims to provide you with a curated list of learning resources and recommendations for various topics including courses, coding platforms, and more.

    Explore the different sections of our platform to discover learning opportunities tailored to your interests and needs.

    ### Get Started

    Use the sidebar to navigate through different sections of the app and start your learning journey today!

    ### Contact Us

    Have questions or feedback? Check out our Contact page to reach out to us.
    """)


	elif selected == "courserecommendation":
		st.subheader("Recommend Courses")
		cosine_sim_mat = vectorize_text_to_cosine_mat(df['Course Name'])
		search_term = st.text_input("Search")
		if st.button("Recommend"):
			if search_term is not None:
				try:
					results = get_recommendation(search_term,cosine_sim_mat,df,5)
					with st.beta_expander("Results as JSON"):
						results_json = results.to_dict('index')
						st.write(results_json)

					for row in results.iterrows():
						rec_title = row[1][0]
						rec_score = row[1][1]
						rec_url = row[1][2]
						rec_num_sub = row[1][4]

						# st.write("Title",rec_title,)
						stc.html(RESULT_TEMP.format(rec_title,rec_score,rec_url,rec_url,rec_num_sub),height=350)
				except:
					results= "Not Found"
					st.warning(results)
					st.info("Suggested Options include")
					result_df = search_term_if_not_found(search_term,df)
					st.dataframe(result_df)
	elif selected == "Consistency":
		st.title("Consistency Development!!")
		
		codingProblems10 = ['Write a program to find even or odd','Write a program to Print 1 to 10 number',
					  'write a program which prints Welcome message.','Write a program to find sum of numbers']
		codingProblems18 = ['Develop a web application for managing tasks using a front-end framework.','Write a program to implement a sorting algorithm of your choice.',
					   'Create a RESTful API for a user authentication system.','Write a program to print the first 10 prime numbers.','Create a function to find the maximum element in an array.',
					   'Implement a simple game using Python.']
		mathProblems10 = ['Solve the equation: 3x + 7 = 16.','Calculate the area of a rectangle with length 5 and width 8.',
					 'Find the square root of 81.','find the area of rectangel whose length id 10cm and breadth is 8cm',
					 'Find the area of a square whose side is 10cm.']
		mathProblems18 = ['Solve a system of linear equations with three variables.','Calculate the definite integral of a given mathematical function.',
					'Prove the Pythagorean theorem using geometry.','Write the procedure to find the determinent of a matrix',
					'Write the Procedure to find the Psuedo inverse of a matrix','What is PCA, Explain how to find Principle components']

		proverbs = ['A stitch in time saves nine.','Actions speak louder than words.','Don’t count your chickens before they hatch.',
			  'Todays future is tomorrows present','Rome was not build in a day',]
		n=random.randint(0,4)
		choice=st.radio("Select Your age Group",["8-15","15-22"])
		if choice=="8-15":
			c=st.radio("Select Your domain",["math","coding"])
			if c=="math":
				st.markdown("Today's Problem:")
				st.markdown(mathProblems10[n])
				st.markdown("Today's Proverb:")
				st.markdown(proverbs[n])
			if c=="coding":
				st.markdown("Today's Problem:")
				st.markdown(codingProblems10[n])
				st.markdown("Today's Proverb:")
				st.markdown(proverbs[n])
		if choice=="15-22":
			c=st.radio("Select Your domain",["math","coding"])
			if c=="math":
				st.markdown("Today's Problem:")
				st.markdown(mathProblems18[n])
				st.markdown("Today's Proverb:")
				st.markdown(proverbs[n])
			if c=="coding":
				st.markdown("Today's Problem:")
				st.markdown(codingProblems18[n])
				st.markdown("Today's Proverb:")
				st.markdown(proverbs[n])

				  

		
	elif selected == "Learn":
		st.title("Learning Platforms")
		st.markdown("Explore various learning platforms:")
		st.markdown("#### General Learning Platforms")
		st.write("These platforms offer a wide range of courses on various topics.")
		# Displaying general learning platforms
		with st.container():
			col1, col2, col3 = st.columns(3)
			with col1:
				st.image("coursera.png", caption='', width=150)
				st.write("[Coursera](https://www.coursera.org/)")
			with col2:
				st.image("edx.png", caption='', width=200)
				st.write("[edX](https://www.edx.org/)")
			with col3:
				st.image("udemy.png", caption='', width=200)
				st.write("[Udemy](https://www.udemy.com/)")


		st.markdown("#### Platforms to Practice Coding")
		st.write("Improve your coding skills with these platforms.")

        # Displaying coding platforms
		with st.container():
			col1, col2, col3 = st.columns(3)
			with col1:
				st.image("geek.png", caption='', width=150)
				st.write("[Geeks for Geeks](https://www.geeksforgeeks.org/)")
			with col2:
				st.image("hackerrank.png", caption='', width=150)
				st.write("[HackerRank](https://www.hackerrank.com/)")
			with col3:
				st.image("codechef.png", caption='', width=150)
				st.write("[CodeChef](https://www.codechef.com/)")
	
	elif selected == "Doubtclearance":
		st.title("Need Help!")
		client = OpenAI(api_key="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")
		if "openai_model" not in st.session_state:
			st.session_state["openai_model"] = "gpt-3.5-turbo"
			
		if "messages" not in st.session_state:
			st.session_state.messages = []
			
		for message in st.session_state.messages:
			with st.chat_message(message["role"]):
				st.markdown(message["content"])
				
		if prompt := st.chat_input("What is up?"):
			st.session_state.messages.append({"role": "user", "content": prompt})
			
			with st.chat_message("user"):
				st.markdown(prompt)
				
			with st.chat_message("assistant"):
				
				stream = client.chat.completions.create(
					model=st.session_state["openai_model"],
					messages=[
						{"role": m["role"], "content": m["content"]}
						for m in st.session_state.messages
                    ],
					stream=True,
                )
				response = st.write_stream(stream)
			st.session_state.messages.append({"role": "assistant", "content": response})
	else:
		#st.markdown("For More details contact:")
		#st.markdown("Upagna Duba "+"22951a66g0@iare.ac.in")
		#st.markdown("Vyshnavi P "+"22951a66j1@iare.ac.in")
		st.title("To Contact")
		st.write("- **Email**: contact@example.com")
		st.write("- **Phone**: +1234567890")
		st.write("### Social Media")
		st.write("- [Twitter](https://twitter.com/example)")
		st.write("- [Facebook](https://facebook.com/example)")
		st.write("- [Instagram](https://instagram.com/example)")


if __name__ == '__main__':
	main()