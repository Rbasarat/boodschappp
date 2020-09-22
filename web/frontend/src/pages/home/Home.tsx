import React, { useState } from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Container, Grid } from "@material-ui/core";
import Logo from "../../components/logo";
import Search from "../../components/search";
import Stores from "../../components/stores";
import { StoresProvider } from "../../context/storeContext";

const useStyles = makeStyles(() => ({
  root: {
    flexGrow: 1,
  },
  grid: {
    minHeight: "100vh",
  },
  mbottom: {
    marginBottom: "2em",
  },
  title: {
    textAlign: "center",
    marginBottom: "2em",
  },
  welcomeText: {
    margin: 0,
  },
}));

const initialState = [
  { store: "ah", active: false, products: [] },
  { store: "deen", active: false, products: [] },
  { store: "dirk", active: false, products: [] },
];

const Home: React.FC = () => {
  const classes = useStyles();

  return (
    <Container>
      <StoresProvider>
        <Grid container item direction="column" alignItems="center" justify="center" className={classes.grid}>
          <Grid container item direction="column" alignItems="center" justify="center" className={classes.title}>
            <h2 className={classes.welcomeText}>Welkom bij</h2>
            <Logo />
          </Grid>
          <Grid item container xs={12} alignItems="center" justify="center" className={classes.mbottom}>
            <Stores />
          </Grid>
          <Grid container item xs={12} alignItems="center" justify="center" className={classes.mbottom}>
            <Search />
          </Grid>
        </Grid>
      </StoresProvider>
    </Container>
  );
};

export default Home;
