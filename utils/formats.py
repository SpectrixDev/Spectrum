GUILD_MESSAGE = """
COMMAND:    {ctx.command}
AUTHOR:     ID: {ctx.author.id}   NAME: {ctx.author}
CHANNEL:    ID: {ctx.channel.id}   NAME: #{ctx.channel}
GUILD:      ID: {ctx.guild.id}   NAME: {ctx.guild}    MEMBER_COUNT: {ctx.guild.member_count}
INVOCATION: {ctx.message.clean_content}
ERROR:
{error}
"""

DM_MESSAGE = """
COMMAND:    {ctx.command}
AUTHOR:     ID: {ctx.author.id} NAME: {ctx.author}
INVOCATION: {ctx.message.clean_content}
ERROR:
{error}
"""

COMMAND_MESSAGE = """
COMMAND:    {ctx.command}
AUTHOR:     ID: {ctx.author.id} NAME: {ctx.author}
INVOCATION: {ctx.message.clean_content}
"""


GUILD_COMMAND_MESSAGE = """
COMMAND:    {ctx.command}
AUTHOR:     ID: {ctx.author.id}  NAME: {ctx.author}
CHANNEL:    ID: {ctx.channel.id}  NAME: #{ctx.channel}
GUILD:      ID: {ctx.guild.id}  NAME: {ctx.guild}  MEMBER_COUNT: {ctx.guild.member_count}
INVOCATION: {ctx.message.clean_content}
"""


GUILD_STATUS_MESSAGE = """
{type} guild
GUILD: NAME {guild.name}  ID: {guild.id}
OWNER: NAME {guild.owner} ID: {guild.owner.id}
MEMBER COUNT: ALL:{guild.member_count} BOTS:{bots} HUMANS:{humans}
CREATED_AT: {guild.created_at}
"""