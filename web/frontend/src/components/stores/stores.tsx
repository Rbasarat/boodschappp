import { makeStyles } from "@material-ui/core/styles";
import { Grid } from "@material-ui/core";
import React, { useState } from "react";
import { arch } from "os";

const useStyles = makeStyles(() => ({
  logo: {
    width: "100%",
    height: "100%",
  },

  gridList: {
    flexWrap: "nowrap",
    // Promote the list into his own layer on Chrome. This cost memory but helps keeping high FPS.
    transform: "translateZ(0)",
  },
  marginBottom: {
    marginBottom: "1em",
  },
}));
const Stores: React.FC = () => {
  const classes = useStyles();

  const [stores, setStore] = useState([
    { store: "ah", active: false, products: [] },
    { store: "deen", active: false, products: [] },
    { store: "dirk", active: false, products: [] },
  ]);

  const updateStore = (id: string) => {
    const newArr = [...stores];
    newArr.map((item) => {
      if (item.store == id) {
        item.active = !item.active;
        return item;
      }
    });

    setStore(newArr);
  };

  return (
    <Grid container direction="column" alignItems="center" justify="center">
      <div className={classes.marginBottom}>Selecteer de supermarkten die je wilt vergelijken</div>
      <Grid container direction="row" alignItems="center" justify="center" spacing={2}>
        <Grid item xs={3} md={1}>
          <img
            id="ah"
            src="/icons/ah_logo.svg"
            alt="Boodschappp logo"
            className={classes.logo}
            onClick={() => {
              updateStore("ah");
              console.log(stores[0]);
            }}
          />
        </Grid>
        <Grid item xs={3} md={1}>
          <img
            src="/icons/deen_logo.svg"
            alt="Boodschappp logo"
            className={classes.logo}
            onClick={() => {
              updateStore("dirk");
              console.log(stores[0]);
            }}
          />
        </Grid>
        <Grid item xs={3} md={1}>
          <img
            src="/icons/dirk_logo.svg"
            alt="Boodschappp logo"
            className={classes.logo}
            onClick={() => {
              updateStore("deen");
              console.log(stores[0]);
            }}
          />
        </Grid>
      </Grid>
    </Grid>
  );
};

export default Stores;
