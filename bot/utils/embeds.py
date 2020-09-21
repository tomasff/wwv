import discord

class BaseEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_footer(text='This is NOT an offical service from the University of Warwick')
        self.colour = discord.Colour.from_rgb(91, 48, 105)

def build_verify_embed(thumbnail_url, link):
    verify = BaseEmbed(title='Verification')

    verify.set_thumbnail(url=thumbnail_url)

    what_next_msg = ('Upon clicking on the link below you will be redirected to a page where you can'
                ' '
                'consent if you allow WW Verify to verify your affiliation with the University.')

    data_stored_msg = ('WW Verify stores very little information: a cryptographic hash of your student ID'
                ' '
                '(necessary so that a Warwick ITS account can only be used to verify one Discord account)'
                ' '
                'and your Discord unique ID.')

    verify.add_field(name='What next?', inline=False, value=what_next_msg)
    verify.add_field(name='What data do we store?', inline=False, value=data_stored_msg)
    verify.add_field(name='Link', value=link)

    return verify

LOADING = BaseEmbed(title='<a:loading:755494890070081656> Waiting for confirmation')
ACCOUNT_VERIFIED = BaseEmbed(title='✅ Account verified and role added')