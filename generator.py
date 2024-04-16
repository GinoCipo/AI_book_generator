import json
from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

client = OpenAI(api_key="")

def names_to_string(names):
    if len(names) == 0:
        return ""
    elif len(names) == 1:
        return names[0]
    else:
        return ", ".join(names[:-1]) + " and " + names[-1]

f = open("new-api/data.json")
data = json.load(f)
f.close()
minds = names_to_string(data["Minds"])
topic = data["Topic"]
mindQuantity = len(data["Minds"])
opener = f"Write the title for a book about {topic}. Book covers ideas from {minds}. Also, write the titles for: An introduction, {mindQuantity} chapters (describing the main ideas from the minds), final chapter remarking points in common between them and a conclusion. Answer in .json format: {{'title': (title), 'subtitles': [(all of the subtitles)] }}. Don't send ANYTHING besides .json response."

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

titles = completion_with_backoff(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a book writing assistant."},
        {"role": "user", "content": opener}
    ]
)

response = json.loads(titles.choices[0].message.content)

prompts = []
contents = []

for index, subtitle in enumerate(response['subtitles']):
    if index == 0:
        intro_prompt = f"Write the content for {subtitle}. DON'T write any subtitle when starting. Be brief and concise. 1 paragraph max."
        prompts.append(intro_prompt)
        intro_completion = completion_with_backoff(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a skillful book writer."},
                {"role": "user", "content": intro_prompt}
            ]
        )
        contents.append(intro_completion.choices[0].message.content)
    elif index == len(response['subtitles'])-1:
        conclusion_prompt = f"Write the content for {subtitle}. DON'T write any subtitle when starting. Be brief and concise. 2 paragraph max."
        prompts.append(conclusion_prompt)
        conclusion_completion = completion_with_backoff(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a skillful book writer."},
                {"role": "user", "content": conclusion_prompt}
            ]
        )
        contents.append(conclusion_completion.choices[0].message.content)
    else:
        chapter_prompt = f"Write the content for {subtitle}. DON'T write any subtitle when starting. Be detailed. 3 paragraph max."
        prompts.append(chapter_prompt)
        chapter_completion = completion_with_backoff(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a skillful book writer."},
                {"role": "user", "content": chapter_prompt}
            ]
        )
        contents.append(chapter_completion.choices[0].message.content)

with open(f"output/{response['title']}.txt", 'w') as f:
    print(response['title'], file=f)
    print("\n", file=f)
    for index, p in enumerate(contents):
        print(response['subtitles'][index], file=f)
        print(p, file=f)
        print("\n", file=f)
    

print("DONE!")
# introduction = "Embarking on Your Investment Journey is an exciting and rewarding endeavor that can help you achieve your financial goals and secure a stable future. Understanding the principles of investing, the various asset classes, and developing a solid investment strategy are crucial steps towards building a successful investment portfolio. By taking the time to educate yourself and make informed decisions, you can navigate the world of investing with confidence and embark on a path to long-term financial growth."
# chapter_1 = """Warren Buffett's Investment Philosophy
#                 Warren Buffett, often referred to as the "Oracle of Omaha," is renowned for his unique and successful investment philosophy. Central to Buffett\'s approach is the concept of value investing, which emphasizes the importance of carefully analyzing a company's intrinsic value before making investment decisions. Buffett looks for companies with strong fundamentals, a durable competitive advantage, and a proven track record of consistent and reliable performance.
#                 Moreover, Buffett advocates a long-term perspective when it comes to investing. He believes in buying and holding onto quality businesses for an extended period, benefiting from their growth and compounding returns over time. This approach is in sharp contrast to short-term trading strategies and speculation, which Buffett famously derides as mere "gambling."
#                 Another key aspect of Buffett's investment philosophy is his emphasis on integrity, honesty, and discipline in all aspects of business dealings. Buffett places a high value on ethical behavior and transparency, both in the companies he invests in and in his own decision-making process. By adhering to these principles, Buffett has built a reputation as one of the most successful and respected investors in the world, with a net worth in the billions and a track record of consistent outperformance in the stock market."""
# chapter_2 = """Adam Smith's Insights on Market Participation
#                 In Chapter 2, we delve into Adam Smith's groundbreaking insights on market participation. Smith, considered the father of modern economics, emphasized the importance of individuals engaging in market transactions to promote economic growth and prosperity. According to Smith, when individuals freely participate in markets, pursuing their self-interest, the overall economy benefits through the principle of the invisible hand. This concept suggests that individuals, by seeking their own gain, unintentionally contribute to the common good of society.\n\nAdam Smith also highlighted the significance of competition in market participation. He argued that competition among individuals and businesses leads to greater efficiency, lower prices, and innovation. Smith believed that through competition, markets are able to allocate resources effectively and drive economic progress. Furthermore, Smith's insights on market participation emphasize the role of specialization and division of labor in enhancing productivity. By focusing on their unique skills and capabilities, individuals can contribute to the economy in a more efficient and specialized manner, leading to overall growth and development.\n\nIn conclusion, Adam Smith's insights on market participation continue to shape economic theory and policy to this day. His emphasis on individual self-interest, competition, and specialization underscores the importance of free markets in driving economic success. By understanding and applying Smith's principles, we can gain a deeper appreciation for the dynamics of market participation and its profound impact on economic outcomes."""
# chapter_3 = """Benjamin Graham\'s Principles of Value Investing\n\nBenjamin Graham, often referred to as the "father of value investing," revolutionized the world of finance with his timeless principles. At the core of Graham\'s approach is the concept of seeking out stocks that are undervalued by the market. Graham believed in the importance of conducting thorough fundamental analysis to determine a stock\'s intrinsic value, which would serve as a guide for making intelligent investment decisions. By focusing on the underlying value of a company rather than short-term market fluctuations, Graham encouraged investors to adopt a long-term perspective and remain steadfast in their commitment to value investing.\n\nOne of the key principles championed by Benjamin Graham is the concept of margin of safety. This principle emphasizes the importance of buying securities at a significant discount to their intrinsic value in order to protect against potential downside risk. By only investing when there is a margin of safety present, investors can mitigate the effects of market volatility and uncertainties, ultimately safeguarding their capital. Graham\'s emphasis on margin of safety has become a cornerstone of value investing, guiding investors to prioritize the preservation of capital while seeking attractive investment opportunities.\n\nFurthermore, Benjamin Graham advocated for a disciplined and patient approach to investing, rooted in rational analysis rather than emotional decision-making. He viewed market fluctuations as opportunities to capitalize on undervalued stocks rather than signals for panic selling or irrational exuberance. Graham\'s principles of value investing continue to resonate with investors today, reminding them of the importance of diligence, prudence, and a long-term perspective in navigating the complexities of the financial markets. By adhering to these timeless principles, investors can strive to achieve sustainable, long-term success in their investment endeavors."""
# chapter_4 = """Finding Unison in Diverse Approaches\n\nIn this chapter, we delve into the beauty and complexity of finding unity amongst diverse approaches. Through exploring various perspectives and methodologies, we discover common threads that weave through seemingly disparate ideas. By embracing the differences in approaches, we uncover new layers of understanding and appreciation for the richness of different points of view. Through this exploration, we learn how to harmonize diverse approaches to create a more comprehensive and inclusive way of thinking.\n\nWe examine how different disciplines, such as art, science, philosophy, and psychology, can intersect and complement each other to provide a holistic perspective on complex issues. By integrating these diverse approaches, we gain fresh insights and innovative solutions to longstanding challenges. Through highlighting the interconnectedness of these disciplines, we foster a sense of unity and interconnectedness that transcends traditional boundaries.\n\nUltimately, this chapter challenges us to break free from siloed thinking and embrace the diversity of approaches available to us. By recognizing the value in each perspective and finding common ground, we can cultivate a sense of unity that celebrates the richness of human thought and experience. Through this process, we open ourselves up to a world of possibilities where collaboration and mutual understanding lead us towards a more harmonious and interconnected future."""
# conclusion = """In conclusion, crafting a solid investment strategy is crucial for achieving your financial goals and building wealth over time. By carefully considering your risk tolerance, financial objectives, and investment timeline, you can develop a strategy that aligns with your needs and preferences. Diversifying your investments across different asset classes, regularly reviewing and adjusting your portfolio, and staying informed about market trends are key components of a successful investment strategy. Remember to stay disciplined, patient, and focused on the long-term while navigating the ups and downs of the market to maximize your chances of success.\n\nUltimately, seeking advice from financial professionals, continually educating yourself about investment principles, and staying adaptable in response to changing market conditions will contribute to your overall investment success. By following these guidelines and remaining committed to your strategy, you can work towards achieving your financial aspirations and securing your financial future for years to come."""
