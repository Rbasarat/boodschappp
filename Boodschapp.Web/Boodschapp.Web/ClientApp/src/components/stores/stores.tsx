import { Grid, IconButton } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import React, { useContext } from "react";
import { StoresContext } from "../../context/storeContext";
import { Types } from "../../context/storeReducer";
import { Cancel, CheckCircle } from "@material-ui/icons";
const useStyles = makeStyles(() => ({
  logo: {
    height: "100%",
    width: "100%",
  },
  gridList: {
    flexWrap: "nowrap",
    // Promote the list into his own layer on Chrome. This cost memory but helps keeping high FPS.
    transform: "translateZ(0)",
  },
  marginBottom: {
    marginBottom: "1em",
  },
  gridItem: {
    margin: "10px",
    padding: "10px",
    position: "relative",
  },
  green: {
    color: "green",
    position: "absolute",
    top: "-10px",
    right: "-15px",
  },
  red: {
    color: "red",
    position: "absolute",
    top: "-10px",
    right: "-15px",
  },
}));
const Stores: React.FC = () => {
  const classes = useStyles();
  const { state, dispatch } = useContext(StoresContext);

  const setStoreSelected = (id: string) => {
    dispatch({
      type: Types.setIsSelected,
      payload: {
        id: id,
      },
    });
  };

  const storeImages = state.stores.map((store) => (
    <Grid key={store.id} container xs={3} md={1} className={`${classes.gridItem}`}>
      {store.isSelected ? <CheckCircle className={classes.green} /> : <Cancel className={classes.red} />}
      <img
        id={store.id}
        src={store.logo}
        alt="Winkel logo"
        className={`${classes.logo}`}
        onClick={() => {
          setStoreSelected(store.id);
        }}
      />
    </Grid>
  ));

  return (
    <Grid container direction="column" alignItems="center" justify="center">
      <div className={classes.marginBottom}>Selecteer de supermarkten die je wilt vergelijken</div>
      <Grid container direction="row" alignContent="space-between" justify="center" spacing={2}>
        {state.stores.length > 0 ? (
          storeImages
        ) : (
          <h2>Er zijn op dit moment geen supermarkten beschikbaar. Excuses voor het ongemak.</h2>
        )}
      </Grid>
    </Grid>
  );
};

export default Stores;
