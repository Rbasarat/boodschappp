using Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace Boodschapp.Web.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class StoresController : ControllerBase
    {
        private readonly IStoreService _storeService;

        public StoresController(IStoreService storeService)
        {
            _storeService = storeService;
        }

        public IActionResult Get()
        {
            return Ok(_storeService.GetActiveStores());
        }
    }
}