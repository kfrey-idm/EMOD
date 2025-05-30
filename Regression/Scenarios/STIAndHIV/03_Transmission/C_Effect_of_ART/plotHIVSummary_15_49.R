# SUMMARY: Plot HIV prevalence, incidence rate, mortality rate, and number on ART for ages 15-49 by gender
# INPUT: output/ReportHIVByAgeAndGender.csv
# OUTPUT: figs/HIV_Summary.png


rm( list=ls( all=TRUE ) )
graphics.off()

library(reshape)
library(ggplot2)
library(gridExtra)

ART_YEAR = 2025

fig_dir = 'figs'
if( !file.exists(fig_dir) ) {
    dir.create(fig_dir)
}

dat = read.csv(file.path("output", "ReportHIVByAgeAndGender.csv"))

prevalent.m = melt(dat, 
    id=c("Year", "Gender", "Age"),
    measure=c("Population", "Infected", "On_ART"))

incident.m = melt(dat, 
    id=c("Year", "Gender", "Age"),
    measure=c("Died", "Died_from_HIV", "Newly.Infected"))

Years = unique(prevalent.m$Year)
nYears = 2*floor(length(Years)/2)   # Make it even
midYears = Years[seq(0,nYears-1) %% 2 == 0]   # First is mid-year

# midYear function for stitching half years together
midYear = function(year) {
    if( any(midYears == year) ) {
        return(year)
    }

    idx = which(year == Years)
    stopifnot(idx > 0)
    return( Years[[idx-1]] )
}

prevalent.m = prevalent.m[prevalent.m$Year %in% midYears,]
prevalent.c = cast(prevalent.m, Year + Gender~ variable, sum, subset=(Age>=15 & Age<50))

incident.m$Year = sapply(incident.m$Year, midYear)
incident.c = cast(incident.m, Year + Gender ~ variable, sum, subset=(Age>=15 & Age<50))

both.c = merge(prevalent.c, incident.c, by=c("Year", "Gender"))
both.c$Prevalence = 100 * both.c$Infected / both.c$Population
both.c$IncidenceRate = both.c$Newly.Infected / (both.c$Population - both.c$Infected)
both.c$IncidenceRate[ is.nan(both.c$IncidenceRate) ] = 0
both.c$HIVCauseMortalityRate = both.c$Died_from_HIV / both.c$Population
both.c$ARTCoverage = 100 * both.c$On_ART / both.c$Infected
both.c$ARTCoverage[ is.nan(both.c$ARTCoverage) ] = 0
both.c$Gender = factor(both.c$Gender, labels=c("Male", "Female"))

# set female incidence rate to zero in seed year to avoid meaningless spike upon seeding infections
both.c$IncidenceRate[is.na(both.c$IncidenceRate) & both.c$Gender=='Female'] <- 0
both.c$IncidenceRate[both.c$Year==2020.5 & both.c$Gender=='Female'] <- NA

p.prevalence = ggplot(both.c, aes(x=Year, y=Prevalence, colour=Gender)) +
    geom_line() +
    geom_vline(xintercept=ART_YEAR, colour="black", linetype="dashed") + # ART in ART_YEAR
    scale_color_manual(values=c("darkblue", "darkred")) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    theme(legend.position=c(0.75,0.9)) +
    theme(legend.title=element_blank()) +
    xlab( "Year" ) +
    ylab( "Prevalence 15-49 (%)" ) +
    ggtitle( "Prevalence" )

p.incidence = ggplot(both.c, aes(x=Year, y=IncidenceRate, colour=Gender)) +
    geom_line() +
    geom_vline(xintercept=ART_YEAR, colour="black", linetype="dashed") + # ART in ART_YEAR
    scale_color_manual(values=c("darkblue", "darkred")) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    theme(legend.position="none") +
    theme(legend.title=element_blank()) +
    xlab( "Year" ) +
    ylab( "Incidence Rate 15-49 (Infections/Susceptible-PY)" ) +
    ggtitle( "Incidence" )

p.deaths = ggplot(both.c, aes(x=Year, y=HIVCauseMortalityRate, colour=Gender)) +
    geom_line() +
    geom_vline(xintercept=ART_YEAR, colour="black", linetype="dashed") + # ART in ART_YEAR
    scale_color_manual(values=c("darkblue", "darkred")) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    theme(legend.position="none") +
    theme(legend.title=element_blank()) +
    xlab( "Year" ) +
    ylab( "HIV-Cause Mortality Rate 15-49 (Deaths/PY)" ) +
    ggtitle( "Mortality" )

p.ART = ggplot(both.c, aes(x=Year, y=ARTCoverage, colour=Gender)) +
    geom_line() +
    geom_vline(xintercept=ART_YEAR, colour="black", linetype="dashed") + # ART in ART_YEAR
    scale_color_manual(values=c("darkblue", "darkred")) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
    theme(legend.position="none") +
    theme(legend.title=element_blank()) +
    xlab( "Year" ) +
    ylab( "Antiretroviral Therapy Coverage (%)" ) +
    ggtitle( "ART" )

q = grid.arrange(p.prevalence, p.incidence, p.deaths, p.ART, ncol=4)

ggsave(file.path(fig_dir,"HIV_Summary.png"), plot=q, width=8, height=4)
