from functions import *
from configs import *

st.set_page_config(
    page_title="DocSwap",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="🔄",
)


gs_connection = connect_to_gs(st.secrets["gcp_service_account"])
all_swap_data = fetch_swap_data(
    gs_connection, find_swap_table, prod_google_sheet_key, []
)
user_status_data = fetch_status_data(
    gs_connection, status_table, prod_google_sheet_key, []
)
latest_swap_data = get_latest_record_per_email(all_swap_data)
unique_users = count_unique_values(all_swap_data, "email")
unique_swaps = count_unique_values_swapped_yes(user_status_data, "email")

st.markdown(
    """
             #### Welcome to DocSwap! 👋"""
)

# st.markdown(
#     """
#             #### Welcome to DocSwap! 👋

#             ⏳ DocSwap will officially open once the 2024  internship placements are out.

#             🗣️ DocSwap works better with more people, share it with other doctors going into their first year of Internship!

#             👀 In the meantime, feel free to check out the info tab to see how DocSwap works or reach out [here](https://docs.google.com/forms/d/e/1FAIpQLSfnt0Dq7JBlw-tEUyfVXJueT8aqE3rAcwxoXWWjWi1Jl88gTw/viewform?usp=sf_link) if you have any questions.


#             """
# )

tab1, tab2 = st.tabs(["Swap", "Info"])

with tab1.expander("🔍 Find a SwapGroup", expanded=False):
    st.markdown(
        """
            🚨 **IMPORTANT:** DocSwap only works for **MBChB** students who are going into their **first** year of internship.

        """
    )

    st.markdown(
        """
            #### Please confirm the following to submit your choices:
        """
    )

    mbchb = st.checkbox("I studied MBChB.")
    intern1 = st.checkbox("I am going into my first year of internship.")
    disclaimer = st.checkbox("I have read the disclaimer.")

    if mbchb and intern1 and disclaimer:
        st.markdown(
            """ Please provide your choices in this [Google form](https://forms.gle/1DggkBb6x2nwJCXC7). You will get an email from us if we find a valid swap for you!"""
        )

with tab1.expander("📊 Swap Statistics", expanded=False):
    space1, column, space2 = st.columns([0.1, 0.8, 0.1])
    with column:
        metrics_container = st.container()
        with metrics_container:
            render_svg_banner(
                "diagrams/stats_banner.svg",
                width=100,
                height=100,
                swappers=unique_users,
                emails=unique_swaps,
            )
        st.markdown("""#### """)
        charts_container = st.container()
        with charts_container:
            hist = (
                alt.Chart(
                    latest_swap_data, title="Number of Posts per Hospital on DocSwap"
                )
                .mark_bar()
                .configure_mark(color="#A398F0")
                .encode(
                    alt.X("count():Q", axis=alt.Axis(title="Number of Posts")),
                    alt.Y(
                        "current_placement:O",
                        axis=alt.Axis(title="Hospital"),
                        sort="-x",
                    ),
                    alt.Order("count():Q", sort="descending"),
                )
            )
            st.altair_chart(
                hist,
                use_container_width=True,
            )


with tab1.expander("🚨 Disclaimer", expanded=True):
    st.markdown(
        """
            1. Swaps are not guaranteed.
            2. Swaps require **everyone** in a SwapGroup to participate, if anyone in a SwapGroup backs out, the group will be invalid and you will need to resubmit your choices so that you can be paired with another SwapGroup.
            3. DocSwap does not manage the logistics of the swap, we simply connect you to a group of valid swappers. You will still need to complete the necessary adminstrative procedures to formalise your swap.
            4. DocSwap takes no responsibility for failed swaps.
    """
    )


with tab2.expander("🤔 How does DocSwap work?"):
    st.markdown("### ")
    row1 = st.container()
    row2 = st.container()
    row3 = st.container()

    with row1:
        (
            col1,
            col2,
        ) = st.columns(2)

        with col1:
            image_container = st.container()
            with image_container:
                render_svg(
                    "diagrams/5wayswap.svg",
                    width=90,
                    height=None,
                    caption=None,
                )

        with col2:
            st.markdown(
                """
                        If we think about a swap visually, it's essentially just a closed loop between a group of people. It doesn't matter how many people are in the loop as long as its closed. DocSwap uses your current placement and your three choices to find loops for you. This also allows for much bigger swaps. The biggest swap we've managed to simulate was a 28-way swap, but typically they are around 2-10 people. 
                        """
            )
        st.markdown("### ")
        st.divider()

    with row2:
        (
            col3,
            col4,
        ) = st.columns(2)

        with col3:
            image_container = st.container()
            with image_container:
                render_svg(
                    "diagrams/incomplete.svg",
                    width=90,
                    height=None,
                    caption=None,
                )

        with col4:
            st.markdown(
                """
                As mentioned above, a swap is a **closed** loop of people. If anyone decides not to proceed with the swap, the chain is broken and you will all need to re-apply for a new SwapGroup. To do this you can just repeat the submission process on the Swap page and you will be added back to the selection pool for swapping.

                """
            )

        st.markdown("### ")
        st.divider()

    with row3:
        (
            col5,
            col6,
        ) = st.columns(2)

        with col5:
            image_container = st.container()
            with image_container:
                render_svg(
                    "diagrams/8wayswap.svg",
                    width=90,
                    height=None,
                    caption=None,
                )

        with col6:
            st.markdown(
                """ When we add more people and give each person multiple choices, the number of closed loops we can create becomes exponentially higher. In this image alone we can create 22 closed loops.\nSo how does DocSwap decide on the best loop? Well we give each arrow a weight corresponding to your choice number (eg. choice 1 will get a weight of 1 and choice 2 will get a weight of 2...) and we find the loops with the lowest total weight! Meaning that higher choices are prioritised.
                """
            )

        st.markdown(
            "This also means loops might not contain everyones first choice, since you might need someones third choice to close the loop. So you're probably wondering how you can beat the system? Well we'll tell you, if you are really set on a specific hospital you can choose that hospital for all 3 of your choices... But there's a catch, in doing this you significantly reduce the number of people you can swap with and so your chances of finding a swap group also decrease."
        )

with tab2.expander("💬 Frequently asked questions", expanded=False):
    st.markdown(
        """
                **Q: Someone in my SwapGroup decided they no longer wanted to swap. What should I do now?**\n
                A: Everyone in the SwapGroup will need to re-apply on the Swap page so that we can find alternative SwapGroups for you.
        """
    )

    st.divider()

    st.markdown(
        """
                **Q: I have already swapped but feel I can still do better, can I swap again?**\n
                A: Yes, you can swap as many times as you want, just make sure you re-apply with your latest placement.
        """
    )

    st.divider()

    st.markdown(
        """
                **Q: How does DocSwap make money?**\n
                A: It doesn't.
        """
    )

    st.divider()

    st.markdown(
        """
                **Q: Do you sell our email addresses or other data?**\n
                A: No, all information is confidential.
        """
    )

    st.divider()

    st.markdown(
        """
                **Q: Will submitting mutliple times give me more choices or better odds at finding a SwapGroup**\n
                A: No, I only take the latest submission per user.
        """
    )


with tab2.expander("📞 Contact us?", expanded=False):
    st.markdown(
        """
                Reach out using this [FORM](https://docs.google.com/forms/d/e/1FAIpQLSfnt0Dq7JBlw-tEUyfVXJueT8aqE3rAcwxoXWWjWi1Jl88gTw/viewform?usp=sf_link) and we'll get back to you.

        """
    )

# gs_connection = connect_to_gs(st.secrets["gcp_service_account"])
# all_swap_data = fetch_swap_data(
#     gs_connection, find_swap_table, prod_google_sheet_key, []
# )
# latest_swap_data = get_latest_record_per_email(all_swap_data)
# unique_users = count_unique_values(all_swap_data, "email")

# pivot_choices = pivot_and_rename_choices(latest_swap_data)

# update_time = time_since_last_update()

# time_to_update = time_until_specified_time(update_time)


# tab1, tab2, tab3 = st.tabs(["Swap", "Stats", "About"])

# with tab1.expander("🔍 Find a SwapGroup?", expanded=False):
#     st.markdown(
#         """
#             🚨 **IMPORTANT:** DocSwap only works for **MBChB** students who are going into their **first** year of internship. We apologise for any inconvenience caused, this is version 1 of DocSwap and we aim to improve it in the future.

#         """
#     )

#     st.markdown(
#         """
#             #### 🤔 Please confirm the following to submit your choices:
#         """
#     )

#     mbchb = st.checkbox("I studied MBChB.")
#     intern1 = st.checkbox("I am going into my first year of internship.")
#     disclaimer = st.checkbox(
#         "I have read the disclaimer below tab **and** the notice above."
#     )

#     if mbchb and intern1 and disclaimer:
#         st.markdown(
#             """ Please provide your choices in this [Google form](https://docs.google.com/forms/d/e/1FAIpQLSfkWmsBrxna_T49ZgENPM_1ebKTX7QdFJANArf9SRWLVGXmLw/viewform?usp=sf_link) and we will email you if we find a valid SwapGroup for you!"""
#         )
#         st.markdown("""Good Luck! 🏆🏆🏆""")


# with tab1.expander("🚨 Disclaimer", expanded=True):
# st.markdown(
#     """
#             1. Swaps are not guaranteed.
#             2. Swaps require **everyone** in a SwapGroup to participate, if anyone in a SwapGroup backs out, the group will be invalid and you will need to resubmit your choices so that you can be paired with another SwapGroup.
#             3. DocSwap **does not** manage the logistics of the swap, we simply connect you to a group of valid swappers.
#             4. It is up to you to lias with your SwapGroup via WhatsApp, Email etc... to finalise the swaps.
#             5. DocSwap receives no monetary incentive for this service nor does it sell user information.
#             6. We take no responsibility for failed swaps or administration errors.
#     """
# )

# with tab2:
#     metrics_container = st.container()
#     with metrics_container:
#         col1, col2, col3, col4 = st.columns(4)

#         col1.metric("Swappers on DocSwap", unique_users)
#         col2.metric("Successful Swaps", 85)
#         col3.metric("Failed Swaps", 13)
#         col4.metric(
#             "Next Refresh",
#             time_to_update,
#             help="The stats on this page are updated every 60 minutes",
#         )

#     charts_container = st.container()
#     with charts_container.expander(
#         "👀 See which posts people are swapping?", expanded=False
#     ):
#         hist = (
#             alt.Chart(latest_swap_data)
#             .mark_bar()
#             .configure_mark(color="#A398F0")
#             .encode(
#                 alt.X(
#                     "current_placement:O", axis=alt.Axis(title="Hospital"), sort="-y"
#                 ),
#                 alt.Y("count():Q", axis=alt.Axis(title="Number of Posts")),
#                 alt.Order("count():Q", sort="descending"),
#             )
#         )

#         st.altair_chart(hist, use_container_width=True)

#     with charts_container.expander("🔥 See the most popular hospitals", expanded=False):
#         domain = ["First Choice", "Second Choice", "Third Choice"]
#         range_ = ["#A398F0", "#F2E4FB", "#480F6C"]

#         bar_chart = (
#             alt.Chart(pivot_choices)
#             .mark_bar()
#             .encode(
#                 alt.X("hospital:O", axis=alt.Axis(title="Hospital"), sort="-y"),
#                 alt.Y("count():Q", axis=alt.Axis(title="Number of Requests")),
#                 alt.Order("count():Q", sort="descending"),
#                 alt.Color(
#                     "choice:N",
#                     scale=alt.Scale(domain=domain, range=range_),
#                     legend=alt.Legend(orient="top", direction="horizontal", title=None),
#                 ),
#             )
#         )
#         st.altair_chart(bar_chart, use_container_width=True)


# with tab3.expander("🤔 How does DocSwap work?", expanded=False):
#     st.markdown(
#         """
#     #### TLDR:

#     We collect placements and top 3 choices of 1st year internship students from all over the country, we then use a program to find people with matching placement/choices and connect them via email. This is done between 2 and 8 people, and we give priority to swaps where more people get their first choice.

#     """
#     )
#     st.divider()
#     st.markdown("""#### Technical Details:""")

#     row1 = st.container()
#     row2 = st.container()
#     row3 = st.container()

#     with row1:
#         (
#             col1,
#             col2,
#         ) = st.columns(2)

#         with col1:
#             image_container = st.container()
#             with image_container:
#                 render_svg(
#                     "diagrams/5wayswap.svg",
#                     width=90,
#                     height=None,
#                     caption=None,
#                 )
#         with col2:
#             st.markdown(
#                 """
#                         Most swaps are typically done on Facebook or WhatsApp groups, one of the biggest challenges with this is that you cannot keep track of everyone's choices and so it can be tough to coordinate swaps with more than 3 people.

#                         Consider a 3-party swap:

#                         - Person A has Person B's choice but Person B does not have Person A's choice
#                         - So Person A would not consider Swapping with Person B as they would not get their choice in return.
#                         - If Person B could find a third Person with willing to swap with them for Person A's choice they could then Swap with Person A and all 3 parties would be satisfied.

#                         On the left we have a diagram of a 5-party swap, imagine the logistical nightmare to achieve this considering none of them can directly swap with each other
#                     """
#             )
#         st.divider()

#     with row2:
#         (
#             col3,
#             col4,
#         ) = st.columns(2)

#         with col3:
#             image_container = st.container()
#             with image_container:
#                 render_svg(
#                     "diagrams/5wayswap2choice.svg",
#                     width=90,
#                     height=None,
#                     caption=None,
#                 )

#         with col4:
#             st.markdown(
#                 """
#                     This gets exponentially more complex when we add multiple choices for each person. Here we have the same 5-party swap but they each have 2 choices now. \n\nCan you find a way to to swap so that everyone gets their first choice?
#                         \nWhat if each person had 3 choices?
#                         \nWhat if there were 1000 people with 3 choices each?
#                     """
#             )
#         st.divider()
#     with row3:
#         (
#             col5,
#             col6,
#         ) = st.columns(2)

#         with col5:
#             image_container = st.container()
#             with image_container:
#                 render_svg(
#                     "diagrams/8wayswap.svg",
#                     width=90,
#                     height=None,
#                     caption=None,
#                 )

#         with col6:
#             st.markdown(
#                 """
#                         DocSwap Sees through the chaos and finds the best possible possible SwapGroup.\n
#                         And while we are able to get extremely large SwapGroups (Our record is 28 😏), we have limited this to 8 people so that it is more managable for you to coordinate your SwapGroup after you've been connected.\n

#                         🚨 **VERY IMPORTANT:** If one of the people in your swap group backs out, the swap will not work!! You will all need to re enter your details on the swap page to be put in a new SwapGroup.\n
#                         🚨 **EVEN MORE IMPORTANT:** Please make sure you are all onboard before offically swapping. DocSwap will not be held liable for administration errors.
#                     """
#             )


# with tab3.expander("💬 FAQ", expanded=False):
#     st.markdown(
#         """
#                 **Q: I have submitted my details, how long will it take to find a swap?**\n
#                 A: This is heavily dependant on your placement and your choices as we will need to find a suitable match. If you have been waiting multiple days, try changing your choices on the Swaps tab. It may also help to look at the stats tab to see how many spots are available at the locations you've chosen.
#         """
#     )

#     st.divider()

#     st.markdown(
#         """
#                 **Q: How are matches determined when there are  multiple suitable matches?**\n
#                 A: In this case we will take the match that has the best possible choice for all candidates. Ex. if we find a 6-party swap with an average choice of 1.8 and another 6-party swap with some of the original candidates (not all) with an average choice of 1.2 we will use the second swap configuration as it means more people got their first choice.
#         """
#     )

#     st.divider()
#     st.markdown(
#         """
#                 **Q: I have recieved an Email stating a valid SwapGroup has been found for me, what next?**\n
#                 A: The other Swappers will be CC'd in the Email along with a diagram and instructions on how to swap. You should coordinate with them via your method of choice (WhatsApp, Email etc...) to arrange your swaps with your hosipitals.
#         """
#     )

#     st.divider()
#     st.markdown(
#         """
#                 **Q: One of the people in my SwapGroup decided not to swap, what now?**\n
#                 A: SwapGroups will not work unless everyone is onboard, everyone in the group will need to fill in the **re-entry** form on the Swap page.
#         """
#     )
#     st.divider()

#     st.markdown(
#         """
#                 **Q: Do I have to apply to different provinces/districts?**\n
#                 A: No, you can put all your choices wherever you want.\n
#                 *tip: have a look at the stats tab to see if anyone is offering the locations you want.*
#         """
#     )
#     st.divider()

#     st.markdown(
#         """
#                 **Q: I have gone through the FAQ and can't find an answer to my question.**\n
#                 A: Please fill out this [FORM](https://docs.google.com/forms/d/e/1FAIpQLSfnt0Dq7JBlw-tEUyfVXJueT8aqE3rAcwxoXWWjWi1Jl88gTw/viewform?usp=sf_link) to ask a specific question and we'll get in touch with you via email"

#         """
#     )
#     st.divider()
