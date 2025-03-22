import streamlit as st
import random
import requests

class CountryApp:
    def __init__(self):
        if 'countries' not in st.session_state:
            response = requests.get('https://restcountries.com/v3.1/all')
            st.session_state.countries = response.json()
    
    def run(self):
        self.render_header()
        self.handle_app_logic()
    
    def render_header(self):
        st.title("🌍 World Explorer")
        st.markdown("### Explore countries around the world!")
    
    def handle_app_logic(self):
        self.render_search_interface()
    
    def show_country_information(self, country):
        st.markdown("📍 Country Information")
        
        if 'flags' in country and 'png' in country['flags']:
            st.image(country['flags']['png'], caption="Country Flag")
        
        if 'capital' in country:
            st.info(f"🏛️ Capital: {country['capital'][0]}")
        if 'population' in country:
            st.info(f"👥 Population: {country['population']:,}")
        if 'region' in country:
            st.info(f"🌍 Region: {country['region']}")
        if 'languages' in country:
            st.info(f"🗣️ Languages: {', '.join(country['languages'].values())}")

    def render_search_interface(self):
        country_query = st.text_input(
            "Which country would you like to explore today?",
            placeholder="Example: Spain, Germany, Cuba, etc.",
            key="country_search"
        )
        
        attribute_query = st.text_input(
            "What specific information would you like to know about this place?",
            placeholder="Example: Capital, Population, Language, Region, Flag, etc.",
            key="attribute_search"
        )
        
        if st.button("🔍 Explore", key="search_button"):
            if country_query:
                self.handle_country_search(country_query, attribute_query)

    def handle_country_search(self, country_query, attribute_query=None):
        matching_countries = [
            c for c in st.session_state.countries 
            if country_query.lower() in c['name']['common'].lower()
        ]
        
        if matching_countries:
            country = matching_countries[0]
            if attribute_query:
                self.show_specific_attribute(country, attribute_query)
            else:
                self.show_country_information(country)
        else:
            st.error("Country not found. Try another name!")

    def show_specific_attribute(self, country, attribute):
        attribute = attribute.lower()
        if 'population' in attribute:
            st.info(f"👥 Population of {country['name']['common']}: {country['population']:,}")
        elif 'language' in attribute:
            if 'languages' in country:
                st.info(f"🗣️ Languages: {', '.join(country['languages'].values())}")
        elif 'region' in attribute:
            st.info(f"🌍 Region: {country['region']}")
        else:
            self.show_country_information(country)

if __name__ == "__main__":
    app = CountryApp()
    app.run()