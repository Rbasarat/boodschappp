using System.Collections.Generic;
using Domain.EfModels;

namespace Interfaces
{
    public interface IStoreService
    {
        List<GroceryStores> GetActiveStores();
    }
}