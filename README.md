# About

Python scripts which allows an automatic buy order for <a href="https://www.degiro.it/"><b>DeGiro</b></a>. Script aim is to automatize a PAC or saving plans.

<h3>What is DeGiro?</h3>
DEGIRO is a European brokerage company, based in Amsterdam. It was founded in 2008 by a group of five former employees of Binck Bank to service the professional market. Investors can buy and sell such securities as common and preferred stocks, fixed income (bonds), options, mutual funds, warrants, and ETFs via an electronic trading platform or by phone.
<br>
<h3>What is a PAC?</h3>
Accumulation Plan (<b>PAC</b>) is an investment solution based on periodic payments that allows to mitigate market fluctuations. By increasing your base investment regularly, you will see your savings grow over time, getting you closer to your financial goals faster. The best choice to support your investment by containing risks.
<br>
<h3>Why a PAC is so important?</h3>
<ul>
<li> thanks to its flexibility and the possibility of predetermining the amount to be paid, an Accumulation Plan is often preferred by savers who do not have large amounts to invest and can instead count on stable and secure income;</li>
<li>PACs, among their strengths, have the advantage of eliminating the seasonal component of investment in the markets and significantly reducing the risk associated with incorrect timing, as required by the "dollar cost averaging" principle. One of the biggest risks of investing in a single solution is choosing the wrong timing. Investing all your resources at a time when the chosen activity is at its peak could cause a huge loss (financial and emotionally stressful), recoverable in a very long time. The investment with a PAC is instead diluted over rather long durations and therefore the fractional purchases are spread over almost all market conditions;</li>
<li>another advantage - of a more psychological and behavioral nature - is to "force" the investor to set aside a sum constantly;</li>
<li>investing in a PAC allows you not to fall into the so-called "emotion trap". Very often (there are numerous studies that confirm this) the underwriters of a financial instrument decide to invest or disinvest on the basis of the latest trend, with an accentuation of the phenomenon in the presence of high volatility. A situation that leads to the trap of emotionality, which sees the investor invest only when prices are close to maximums or divest when prices are close to minimums.</li>
</ul>

# Libraries

<ul>
    <li>degiroapi;</li>
    <li>json;</li>
    <li>random;</li>
    <li>csv;</li>
    <li>discord_webhook;</li>
    <li>datetime;</li>
    <li>logging;</li>
    <li>discord_webhook;</li>
</ul>

# How to set up
<ol>
<li>Fill configuration file in files/config.json.
<ul>
<li>username:[your DEGIRO <b>username</b>], password:[your DEGIRO <b>password</b>]</li>
<li>amount: the amount you want to invest for each buy time</li>
<li>ETF: for each product you want to buy insert the product id and the percentile (e.g 60). The sum of all percentiles must be 100</li>
<li>webhook: your discord webhook to receive notification about errors or buy orders</li>
</ul>
</li>
<li>Setup a <a href=https://active-directory-wp.com/docs/Usage/How_to_add_a_cron_job_on_Windows/Scheduled_tasks_and_cron_jobs_on_Windows/index.html>crontab</a> or use online service to plan your buy order every weeks/months</li>
</ol>

# Outcome
<ul>
<li>The script automatically save a log of every operation in files/log.log;</li>
<li>Check buy orders in outcome/order_recap.csv;</li>
<li>Check porftfolio status in outcome/portfolio_status.csv;<li>
<li>The script automaticcaly generate a pie chart of your portfolio.</li>
</ul>