# py-statuscake
A simple Python-based SDK for the StatusCake API.

# Introduction
StatusCake provides powerful website monitoring tools that are quick and easy to set-up. Users decide how they want to receive alerts the instant their site goes down; whether by email, SMS, push notifications or 3rd party integrations such as slack.

StatusCake also provide page speed monitoring, providing analysis which can be used to improve page load, increasing conversions and improving SEO.

Other tools include SSL certificate monitoring, domain monitoring, and virus scanning.

# API Reference
The API reference for StatusCake can be found [HERE](https://developers.statuscake.com/api/).

# Getting Started
Simply create a `StatusCakeClient` object, specifying your StatusCake API key. Each of the API calls available at the time of publishing this repo are available as functions of the `StatusCakeClient`.

# Current State
This repo is _*VERY*_ basic right now. I only needed to set up a couple of calls, but had the time to configure the basic Session/Client topology. If I use StatusCake again in the future, I'll continue to update this repo.
