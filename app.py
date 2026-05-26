import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")
st.markdown("""
<style>
       .block-container {
            padding-top: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
</style>
""", unsafe_allow_html=True)
tab1, tab2 , tab3 ,tab4 = st.tabs(["Home", "search&Recommend","Genre" ,"Special"])
@st.cache_resource
def load_data():

    popular_df = pd.read_pickle("populer.pkl")
    books = pd.read_pickle("books.pkl")
    books1 = pd.read_pickle("book1.pkl")
    pt = pd.read_pickle("pt.pkl")
    similarity_scores = pd.read_pickle("similarity_scores.pkl")
    best_genre = pd.read_pickle("best_genre.pkl")

    return popular_df, books, books1, pt, similarity_scores, best_genre


popular_df, books, books1, pt, similarity_scores, best_genre = load_data()


with tab1:
    st.subheader("Most Popular Books Section ⭐")
    col1, col2, col3 = st.columns(3)
    with col1:
         for i in range(0,45,3):
            book_name = popular_df['Book-Title'].iloc[i]
            pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
            st.image(popular_df["Image-URL-M"].iloc[i])
            st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                unsafe_allow_html=True)
            st.write("Book-Author : ", popular_df["Book-Author"].iloc[i])
            st.write("Rating : ", np.round(popular_df["avg_ratings"].iloc[i],2))            
         
              
    with col2:
         for i in range(1,45,3):
            book_name = popular_df['Book-Title'].iloc[i]
            pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
            st.image(popular_df["Image-URL-M"].iloc[i])
            st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                unsafe_allow_html=True)
            st.write("Book-Author : ", popular_df["Book-Author"].iloc[i])
            st.write("Rating : ", np.round(popular_df["avg_ratings"].iloc[i],2))
    with col3:
         for i in range(2,45,3):
            book_name = popular_df['Book-Title'].iloc[i]
            pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
            st.image(popular_df["Image-URL-M"].iloc[i])
            st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                unsafe_allow_html=True)
            st.write("Book-Author : ", popular_df["Book-Author"].iloc[i])
            st.write("Rating : ", np.round(popular_df["avg_ratings"].iloc[i],2))

with tab2:
    def recommend(book_name):
        book_name = book_name.strip().lower()
        pt_index = pt.index.str.strip().str.lower()
        index = np.where(pt_index == book_name)[0][0]
        similer_items = sorted(list(enumerate(similarity_scores[index])),key = lambda x : x[1],reverse = True)[0:5]
        data = []

        for i in similer_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            data.append(item)

        return data
    bookname = st.text_input("enter your favorite book ")
    if bookname:
        if bookname.strip().lower() not in pt.index.str.strip().str.lower().values:
            st.error("This book is not available.")

        else:
            st.success("your favorite book and also some recommendations for you")
            data = recommend(bookname)
        
            col4,col5 = st.columns(2)
            with col4:
                for i in range(0,5,2):
                    book_name = data[i][1]
                    pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
                    st.image(data[i][0])
                    st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                    unsafe_allow_html=True)
                    st.write("Book-Author : ",data[i][2])
            with col5:
                
                for i in range(1,5,2):
                    book_name = data[i][1]
                    pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
                    st.image(data[i][0])
                    st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                    unsafe_allow_html=True)
                    st.write("Book-Author : ",data[i][2])

with tab3:
    def top_books_by_category(category):
        filtered_df = books1[books1['Category'] == category]
        filtered_df = filtered_df.sort_values(by='Stars', ascending=False)
        top5 = filtered_df.head(10)
        result = []
        for _, row in top5.iterrows():  
            book_data = [
                row['Image_Link'],
                row['Title'],
                row['Stars'],
                row['Book_Description']
            ]
            result.append(book_data)
        return result
    
    genres = books1['Category'].unique().tolist()
    selected_genre = st.selectbox("Select your genre",genres)
    if selected_genre:
        top_books = top_books_by_category(selected_genre)
        col6 , col7 = st.columns(2)
        with col6:
            for i in range(0,10,2):
                    book_name = top_books[i][1]
                    pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
                    st.image(top_books[i][0], width=100)
                    st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                    unsafe_allow_html=True)
                    st.write("Rating : ",top_books[i][2])
        with col7:
            for i in range(1,10,2):
                    book_name = top_books[i][1]
                    pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
                    st.image(top_books[i][0], width=100)
                    st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                    unsafe_allow_html=True)
                    st.write("Rating : ",top_books[i][2])
with tab4:
        def find_genre(age , gender, mood):
            x = best_genre[best_genre['Age_Group'] == age]
            y  = x[x['Gender'] == gender]
            z = list(y[y['Mood'] == mood][['Top_1','Top_2','Top_3']].iloc[0])
            return z
        age = st.selectbox("select your age grp",['Under 12','12 to 18','18 to 50','Above 50'])
        gender = st.selectbox("select your gender ",['Male','Female'])
        mood = st.selectbox("how are you current mood now",['Positive','Negative','Neutral'])
        best_on_mood = find_genre(age,gender,mood)
        genre1_books = top_books_by_category(best_on_mood[0])
        genre2_books = top_books_by_category(best_on_mood[1])
        genre3_books = top_books_by_category(best_on_mood[2])
        st.subheader(f"acc to your mood best books : {best_on_mood[0]}")

        col6 , col7 = st.columns(2)
        with col6:
            for i in range(0,4,2):
                    book_name = genre1_books[i][1]
                    pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
                    st.image(genre1_books[i][0], width=100)
                    st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                    unsafe_allow_html=True)
                    st.write("Rating : ",genre1_books[i][2])
        with col7:
            for i in range(1,4,2):
                    book_name = genre1_books[i][1]
                    pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
                    st.image(genre1_books[i][0], width=100)
                    st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                    unsafe_allow_html=True)
                    st.write("Rating : ",genre1_books[i][2])        
        st.subheader(f"other books according to your mood : {best_on_mood[1]} , {best_on_mood[2]}")
        col8 , col9 = st.columns(2)
        with col8:
            for i in range(0,2,2):
                    book_name = genre2_books[i][1]
                    pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
                    st.image(genre2_books[i][0], width=100)
                    st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                    unsafe_allow_html=True)
                    st.write("Rating : ",genre2_books[i][2])
        with col9:
            for i in range(1,2,2):
                    book_name = genre2_books[i][1]
                    pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
                    st.image(genre2_books[i][0], width=100)
                    st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                    unsafe_allow_html=True)
                    st.write("Rating : ",genre2_books[i][2])
        col10 , col11 = st.columns(2)
        with col10:
            for i in range(0,2,2):
                    book_name = genre3_books[i][1]
                    pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
                    st.image(genre3_books[i][0], width=100)
                    st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                    unsafe_allow_html=True)
                    st.write("Rating : ",genre3_books[i][2])
        with col11:
            for i in range(1,2,2):
                    book_name = genre3_books[i][1]
                    pdf_link = f"https://www.google.com/search?q={book_name}+filetype:pdf"
                    st.image(genre3_books[i][0], width=100)
                    st.markdown(f'<a href="{pdf_link}" target="_blank">'f'{book_name}</a>',
                    unsafe_allow_html=True)
                    st.write("Rating : ",genre3_books[i][2])