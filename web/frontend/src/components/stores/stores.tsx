import { makeStyles } from "@material-ui/core/styles";
import { GridList, GridListTile, GridListTileBar } from "@material-ui/core";

import React from "react";
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
}));

const Stores: React.FC = () => {
  const classes = useStyles();
  return (
    <div>
      <text>Selecteer de supermarkten die je wilt vergelijken</text>{" "}
      <GridList className={classes.gridList} cols={12}>
        <GridListTile>
          <img src="/icons/ah_logo.svg" alt="Boodschappp logo" className={classes.logo} />
        </GridListTile>
        <GridListTile>
          <img src="/icons/deen_logo.svg" alt="Boodschappp logo" className={classes.logo} />
        </GridListTile>
        <GridListTile>
          <img src="/icons/dirk_logo2.svg" alt="Boodschappp logo" className={classes.logo} />
        </GridListTile>
      </GridList>
    </div>
  );
};

export default Stores;
