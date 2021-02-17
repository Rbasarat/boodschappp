using Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace Boodschapp.Web.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class StoreController : ControllerBase
    {
        private readonly IStoreService _storeService;

        public StoreController(IStoreService storeService)
        {
            _storeService = storeService;
        }

        public IActionResult Get()
        {
            return Ok(_storeService.GetActiveStores());
        }
    }
}