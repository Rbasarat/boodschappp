import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Container, Grid } from "@material-ui/core";
import Logo from "../../components/logo";
import Search from "../../components/search";
import Stores from "../../components/stores";

const useStyles = makeStyles(() => ({
  root: {
    flexGrow: 1,
  },
  grid: {
    minHeight: "100vh",
  },
  mbottom: {
    marginBottom: "15px",
  },
  title: {
    background: "red",
    textAlign: "center",
  },
  logo: {
    width: "75px",
    marginLeft: "5px",
    marginRight: "5px",
  },
  welcomeText: {
    margin: 0,
  },
}));

const Home: React.FC = () => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Container maxWidth="xl">
        <Grid container direction="column" alignItems="center" justify="center" className={classes.grid}>
          <Grid
            container
            item
            xs={12}
            direction="column"
            alignItems="center"
            justify="center"
            className={classes.mbottom}
          >
            <h2 className={classes.welcomeText}>Welkom bij</h2>
            <Logo />
          </Grid>
          <text>Selecteer de supermarkten die je wilt vergelijken</text>
          <Grid container item xs={12} direction="row" alignItems="center" justify="center" className={classes.mbottom}>
            <Stores />
          </Grid>
          <Grid container item xs={9} direction="row" alignItems="center" justify="center" className={classes.mbottom}>
            <Search />
          </Grid>
        </Grid>
      </Container>
    </div>
  );
};

export default Home;
