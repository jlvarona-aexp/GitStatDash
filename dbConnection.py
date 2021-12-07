import sqlite3

sqlCreatorNames = '''select distinct u.name as "Creator Name" from users as u, CREATORS as c where u.id = c.creator'''

sqlCommenterNames = '''select distinct u.name as "Reviewer Name" from users as u, activity as a where u.id = a.user_id'''

sqlRepos = '''select name as "Repo" from repos'''

sqlTeams = '''select name as "Team" from teams'''

sqlBand = '''select distinct band as "Band" from users'''

sqlCreators = ''' select c.id as "id", 
c.link as "Link", 
r.name as Repo , 
c.name as "Name", 
c.submitted as "Submitted", 
c.done as "Done", 
c.state as "State", 
u.name as Creator, 
t.name as Team, 
c.duration as "Duration", 
c.comments as "Comments",
c.created_at as "Created At",
c.updated_at as "Updated At",
c.merged_at as "Merged At",
c.closed_at as "Closed At",
c.additions as "Additions", 
c.deletions as "Deletions", 
c.changed_files as "Changed Files",
c.draft as "Draft",
u.band as "Band"
from CREATORS as c
left join repos r on c.repo = r.id
left join users as u on c.creator = u.id
left join teams as t on u.team_id = t.id
where u.name not in ('svc.m1automation m1automation', 'Mobile Automation')
order by c.repo, c.id desc '''


sqlActivitiesDiffs = ''' select c.id as "id",
       r.name as "Repo",
       min(a.activity_id) as "Activity Id",
       c.link as "Link",
       c.name as "Name",
       c.submitted as "Submitted",
       c.done as "Done",
       c.state as "State",
       (select u2.name from users as u2 where u2.id = c.creator) as "Creator",
       c.created_at as "Created At",
       c.updated_at as "Updated_At",
       c.merged_at as "Merged At",
       c.closed_at as "Closed At",
       a.action as "Action",
       a.createdDate as "Action Date",
       u.name as "Reviewer",
       (select t.name from teams as t where t.id = u.team_id) as "Team",
       c.duration as "Duration",
       c.additions as "Additions",
       c.deletions as "Deletions",
       c.changed_files as "Changed Files",
       c.draft as "Draft",
       Cast((julianday(a.createdDate) - julianday(c.created_at)) * 24 as Integer) as since_start ,
       Cast((julianday(a.createdDate) - julianday(c.updated_at)) * 24 as Integer) as since_update,
       (select u2.band from users as u2 where u2.id = c.creator) as creatorBand,
       u.band as reviewerBand
from (select * from activity where action = "COMMENTED" group by pr_id order by pr_id, activity_id) as a,
     creators as c,
     repos as r,
     users as u
where a.pr_id = c.pr_id and
        a.user_id = u.id and
        c.repo = r.id and
        c.creator <> a.user_id and
        u.name not in ('svc.m1automation', 'Mobile Automation')
group by a.pr_id
order by c.repo, c.id desc, a.activity_id asc '''


def getDBConnection():
    conn = None
    #'/Users/jvaronaf/Documents/metrics.sqlite'
    conn = sqlite3.connect('/Users/jvaronaf/OneDrive - American Express/metrics.sqlite')
    return conn

