import React, { createContext, useState } from "react";

export const Context = createContext({} as StoresContextType);

type Props = {
  children: React.ReactNode;
};

type StoresContextType = {
  stores: { store: string; active: boolean }[];
  setStoreIsActive: (value: string) => void;
};

const initState = [
  { store: "ah", active: false },
  { store: "deen", active: false },
  { store: "dirk", active: false },
];
export const Provider = (props: Props) => {
  // Initial values are obtained from the props
  const { children } = props;

  // Use State to keep the values
  const [stores, setStores] = useState(initState);

  const setStoreIsActive = (id: string) => {
    const newArr = [...stores];
    newArr.map((item) => {
      if (item.store == id) {
        item.active = !item.active;
        return item;
      }
    });

    setStores(newArr);
  };

  // Make the context object:
  const storesContext = { stores, setStoreIsActive, setStores };

  // pass the value in provider and return
  return <Context.Provider value={storesContext}>{children}</Context.Provider>;
};

export const { Consumer } = Context;
