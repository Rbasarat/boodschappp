import React, { useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Container, Grid } from "@material-ui/core";
import Logo from "../../components/logo";
import Search from "../../components/search";
import Stores from "../../components/stores";
import { InitialStateType, StoresProvider } from "../../context/storeContext";
import axios from "axios";
import { useState } from "react";

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

const Home: React.FC = () => {
  const classes = useStyles();
  const [loading, setIsLoading] = useState<boolean>(true);
  const [stores, setStores] = useState<InitialStateType>({ stores: [] });
  useEffect(() => {
    axios
      .get("http://slowwly.robertomurray.co.uk/delay/3000/url/https://jsonplaceholder.typicode.com/users")
      .then(function (response) {
        console.log(response);
        setStores({
          stores: [
            { id: "ah", active: false, name: "ah" },
            { id: "deen", active: false, name: "deen" },
            { id: "dirk", active: false, name: "dirk" },
          ],
        });
        setIsLoading(false);
      })
      .catch(function (error) {
        console.log(error);
      });
  }, [loading]);
  return (
    <Container>
      <Grid container item direction="column" alignItems="center" justify="center" className={classes.grid}>
        <Grid container item direction="column" alignItems="center" justify="center" className={classes.title}>
          <h2 className={classes.welcomeText}>Welkom bij</h2>
          <Logo />
        </Grid>
        {loading ? (
          <div>Loading data</div>
        ) : (
          <StoresProvider initialState={stores}>
            <Grid item container xs={12} alignItems="center" justify="center" className={classes.mbottom}>
              <Stores />
            </Grid>
            <Grid container item xs={12} alignItems="center" justify="center" className={classes.mbottom}>
              <Search />
            </Grid>
          </StoresProvider>
        )}
      </Grid>
    </Container>
  );
};

export default Home;
