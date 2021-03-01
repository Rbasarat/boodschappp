using System.Collections.Generic;
using System.Linq;
using Domain.EfModels;
using Interfaces;

namespace Services
{
    public class StoreService : IStoreService
    {
        private readonly BoodschapppContext _context;

        public StoreService(BoodschapppContext context)
        {
            _context = context;
        }

        public List<GroceryStores> GetActiveStores()
        {
            return _context.GroceryStores.Where(x => x.IsActive).ToList();
        }
    }
}