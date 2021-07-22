import streamlit as st
#database
import sqlite3
import base64
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os
import io

conn = sqlite3.connect('data.db')
c = conn.cursor()

#Function
def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS blogtable(name TEXT,title TEXT,article TEXT,postdate DATE)')

def add_data(name,title,article,postdate):
    c.execute('INSERT INTO blogtable(name,title,article,postdate) VALUES (?,?,?,?)',(name,title,article,postdate))
    conn.commit()     

def view_all():
    c.execute('SELECT * FROM blogtable')
    data = c.fetchall()
    return data

def view_all_titles():
    c.execute('SELECT DISTINCT title FROM blogtable')
    data = c.fetchall()
    return data

def get_blog_by_title(title):
    c.execute('SELECT * FROM blogtable WHERE title="{}"'.format(title))
    data = c.fetchall()
    return data

def get_blog_by_name(name):
    c.execute('SELECT * FROM blogtable WHERE name="{}"'.format(name))
    data = c.fetchall()
    return data

# def update_data(title):
#     c.execute('UPDATE  blogtable SET  WHERE title="{}"'.format(title))
#     conn.commit()

def delete_data(title):
    c.execute('DELETE  FROM blogtable WHERE title="{}"'.format(title))
    conn.commit()

#Layout Templates

    #file downloading
    
# Examples

title_temp = """

<div style="background-color:#464e5f;padding:10px,margin:10px;border-radius: 12px">
<h4 style="color:white;text-align:center;">{}</h4>
<h4 style="color:white;text-align:center;">{}</h4>
<h4 style="color:white;text-align:center;">Title  : {}</h4>
<p style="color:white;text-align:left;"> Today Task :
   {}</p>
<h6 style="color:white;text-align:center;">Post Date : {}</h6>
<hr>
</div>
"""
head_temp = """
<div style="background-color:#464e5f;padding:10px,margin:10px;border-radius: 12px">
<h4 style="color:white;text-align:center;">{}</h4>
<h4 style="color:white;text-align:center;"> Title  : {}</h4>
<h6 style="color:white;text-align:center;">Post Date : {}</h6>
<hr>
</div>
"""
full_temp = """
<div style="background-color:silver;padding:10px,margin:10px;border-radius: 12px">
<p style="color:black;text-align:left;"> Today Task :
   {}</p>
</div>
"""


def main():
    """A simple Blog Crud"""
    st.title("Python Developer Tasks")
   
    menu = ["Home","View Posts","Add Post","Search","Manage Blog"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice =="Home":
        st.subheader("Home")
       
        result = view_all()
       
        for i in result:
            b_name = i[0]
            b_title = i[1]
            b_article = str(i[2])[0:30]
            b_post_date = i[3]
            st.markdown(title_temp.format(b_post_date,b_name,b_title,b_article,b_post_date),unsafe_allow_html=True)
        
    elif choice =="View Posts":
        st.subheader("View Articles") 
        all_titles = [i[0] for i in view_all_titles()]
        postlist = st.sidebar.selectbox("View Posts",all_titles)
        post_result = get_blog_by_title(postlist)
        for i in post_result:
            b_name = i[0]
            b_title = i[1]
            b_article = i[2]
            b_post_date = i[3]
            st.markdown(head_temp.format(b_name,b_title,b_post_date),unsafe_allow_html=True)
            st.markdown(full_temp.format(b_article),unsafe_allow_html=True)
        if st.button("thanks"):
            st.balloons()        


    elif choice =="Add Post":
        st.subheader("Add Articles")
        create_table()  
        blog_name =st.text_input("Enter Your Name", max_chars=50)
        blog_title = st.text_input("Enter Post Title")
        blog_article = st.text_area("Post Article Here",height=200)
        blog_post_date = st.date_input("Date")
        if st.button("Add"):
            add_data(blog_name,blog_title,blog_article,blog_post_date)
            st.success(f"Post {blog_title} saved.")


   
    elif choice =="Search":
        st.subheader("Search Articles")  
        search_term = st.text_input('Enter Search Term')   
        search_choice = st.radio("Field to search By",("title","name"))  
        if st.button("Search"):


            if search_choice == "title":
                result = get_blog_by_title(search_term)
            elif search_choice == "name":
                result = get_blog_by_name(search_term)  

            for i in result:
                b_name = i[0]
                b_title = i[1]
                b_article = i[2]
                b_post_date = i[3]
                st.markdown(head_temp.format(b_name,b_title,b_post_date),unsafe_allow_html=True)
                st.markdown(full_temp.format(b_article),unsafe_allow_html=True)
                


    elif choice =="Manage Blog":
        st.subheader("Manage Articles")        
        result = view_all()
      
        df = pd.DataFrame(result, columns=["name","title","article","date"])
        towrite = io.BytesIO()
        downloaded_file = df.to_excel(towrite, encoding='utf-8', index=False, header=True)
        towrite.seek(0)  # reset pointe r
        b64 = base64.b64encode(towrite.read()).decode()  # some strings
        linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="myfilename.xlsx">Download excel file</a>'
        st.markdown(linko, unsafe_allow_html=True)
        clean_db = pd.DataFrame(result,columns=["Name","Title","Article","Post Date"])
        st.dataframe(clean_db) 

        Unique_title= [i[0] for i in view_all_titles()]
        delete_blog_by_title = st.selectbox("Unique title",Unique_title)
        
        if st.button("Delete"):
            delete_data(delete_blog_by_title)
            st.warning("Deleted:'{}'".format(delete_blog_by_title))

        


if __name__ =="__main__":
    main()    