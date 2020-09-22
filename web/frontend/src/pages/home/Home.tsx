import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Container, Grid } from "@material-ui/core";
import Logo from "../../components/logo";
import Search from "../../components/search";
import Stores from "../../components/stores";
import { StoresContextProvider } from "../../context";

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
  { store: "ah", active: false },
  { store: "deen", active: false },
  { store: "dirk", active: false },
];

const Home: React.FC = () => {
  const classes = useStyles();
  return (
    <StoresContextProvider>
      <Container>
        <Grid container item direction="column" alignItems="center" justify="center" className={classes.grid}>
          <Grid item container xs={12} alignItems="center" justify="center" className={classes.mbottom}>
            <Stores />
          </Grid>
        </Grid>
      </Container>
    </StoresContextProvider>
  );
};

export default Home;
