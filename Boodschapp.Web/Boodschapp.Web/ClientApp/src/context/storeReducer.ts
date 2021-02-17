type ActionMap<M extends { [index: string]: unknown }> = {
  [Key in keyof M]: M[Key] extends undefined
    ? {
        type: Key;
      }
    : {
        type: Key;
        payload: M[Key];
      };
};

export enum Types {
  setIsActive = "SET_IS_ACTIVE",
}

type StoreType = {
  id: string;
  storeName: string;
  isActive: boolean;
  logo: string;
};

type StorePayload = {
  [Types.setIsActive]: {
    id: string;
  };
};

export type StoreActions = ActionMap<StorePayload>[keyof ActionMap<StorePayload>];

export const storeReducer = (state: StoreType[], action: StoreActions): StoreType[] => {
  switch (action.type) {
    case "SET_IS_ACTIVE":
      return state.map((item) => (item.id === action.payload.id ? { ...item, isActive: !item.isActive } : item));
    default:
      return state;
  }
};
